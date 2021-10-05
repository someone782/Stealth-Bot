import discord
import datetime
import io
import asyncio
import random
import helpers.helpers as helpers
from helpers import paginator
from PIL import Image, ImageSequence
import re
import errors
import aiohttp
from typing import Optional
import typing
from discord.ext import commands, menus
import io
import os
import re
import zlib

from discord.ext.menus.views import ViewMenuPages

def finder(text, collection, *, key=None, lazy=True):
    suggestions = []
    text = str(text)
    pat = '.*?'.join(map(re.escape, text))
    regex = re.compile(pat, flags=re.IGNORECASE)
    for item in collection:
        to_search = key(item) if key else item
        r = regex.search(to_search)
        if r:
            suggestions.append((len(r.group()), r.start(), item))

    def sort_key(tup):
        if key:
            return tup[0], tup[1], key(tup[2])
        return tup

    if lazy:
        return (z for _, _, z in sorted(suggestions, key=sort_key))
    else:
        return [z for _, _, z in sorted(suggestions, key=sort_key)]


class SphinxObjectFileReader:
    # Inspired by Sphinx's InventoryFileReader
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode('utf-8')

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b''
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b'\n')
            while pos != -1:
                yield buf[:pos].decode('utf-8')
                buf = buf[pos + 1:]
                pos = buf.find(b'\n')

def setup(client):
    client.add_cog(Misc(client))
    
UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]


def pretty_size(bytes, units=UNITS_MAPPING):
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix
    
class BotServersEmbedPage(menus.ListPageSource):
    def __init__(self, data, name):
        self.data = data
        self.name = name
        super().__init__(data, per_page=1)
    
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        embed = discord.Embed(title=f"{self.name}", description=entries, timestamp=discord.utils.utcnow(), color=color)
        return embed

class Misc(commands.Cog):
    ":gear: | Miscellaneous commands"
    def __init__(self, client):
        self.client = client
        
    async def build_rtfm_lookup_table(self, page_types):
        cache = {}
        for key, page in page_types.items():
            sub = cache[key] = {}
            async with self.client.session.get(page + '/objects.inv') as resp:
                if resp.status != 200:
                    raise RuntimeError('Cannot build rtfm lookup table, try again later.')

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = self.parse_object_inv(stream, page)

        self._rtfm_cache = cache

    def parse_object_inv(self, stream, url):
        # key: URL
        # n.b.: key doesn't have `discord` or `discord.ext.commands` namespaces
        result = {}

        # first line is version info
        inv_version = stream.readline().rstrip()

        if inv_version != '# Sphinx inventory version 2':
            raise RuntimeError('Invalid objects.inv file version.')

        # next line is "# Project: <name>"
        # then after that is "# Version: <version>"
        projname = stream.readline().rstrip()[11:]
        version = stream.readline().rstrip()[11:]

        # next line says if it's a zlib header
        line = stream.readline()
        if 'zlib' not in line:
            raise RuntimeError('Invalid objects.inv file, not z-lib compatible.')

        # This code mostly comes from the Sphinx repository.
        entry_regex = re.compile(r'(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)')
        for line in stream.read_compressed_lines():
            match = entry_regex.match(line.rstrip())
            if not match:
                continue

            name, directive, prio, location, dispname = match.groups()
            domain, _, subdirective = directive.partition(':')
            if directive == 'py:module' and name in result:
                # From the Sphinx Repository:
                # due to a bug in 1.1 and below,
                # two inventory entries are created
                # for Python modules, and the first
                # one is correct
                continue

            # Most documentation pages have a label
            if directive == 'std:doc':
                subdirective = 'label'

            if location.endswith('$'):
                location = location[:-1] + name

            key = name if dispname == '-' else dispname
            prefix = f'{subdirective}:' if domain == 'std' else ''

            if projname == 'discord.py':
                key = key.replace('discord.ext.commands.', '').replace('discord.', '')

            result[f'{prefix}{key}'] = os.path.join(url, location)

        return result

    async def do_rtfm(self, ctx, key, obj):
        page_types = {
            'latest': 'https://discordpy.readthedocs.io/en/latest',
            'latest-jp': 'https://discordpy.readthedocs.io/ja/latest',
            'python': 'https://docs.python.org/3',
            'python-jp': 'https://docs.python.org/ja/3',
            'master': 'https://discordpy.readthedocs.io/en/master',
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self, '_rtfm_cache'):
            await ctx.trigger_typing()
            await self.build_rtfm_lookup_table(page_types)

        obj = re.sub(r'^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)', r'\1', obj)

        if key.startswith('latest'):
            # point the abc.Messageable types properly:
            q = obj.lower()
            for name in dir(discord.abc.Messageable):
                if name[0] == '_':
                    continue
                if q == name:
                    obj = f'abc.Messageable.{name}'
                    break

        cache = list(self._rtfm_cache[key].items())

        matches = finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

        e = discord.Embed(colour=discord.Colour.blurple())
        if len(matches) == 0:
            return await ctx.send('Could not find anything. Sorry.')

        e.description = '\n'.join(f'[`{key}`]({url})' for key, url in matches)
        await ctx.send(embed=e)

    def transform_rtfm_language_key(self, ctx, prefix):
        if ctx.guild is not None:
            #                             日本語 category
            if ctx.channel.category_id == 490287576670928914:
                return prefix + '-jp'
            #                    d.py unofficial JP   Discord Bot Portal JP
            elif ctx.guild.id in (463986890190749698, 494911447420108820):
                return prefix + '-jp'
        return prefix
    
    @commands.command()
    async def serverlist(self, ctx):
        botServers = self.client.guilds
        servers = []

        for server in botServers:
            
            name = server.name

            if ctx.me.guild_permissions.ban_members:
                bannedMembers = len(await server.bans())
            else:
                bannedMembers = "Couldn't get banned members."

            statuses = [len(list(filter(lambda m: str(m.status) == "online", server.members))),
                        len(list(filter(lambda m: str(m.status) == "idle", server.members))),
                        len(list(filter(lambda m: str(m.status) == "dnd", server.members))),
                        len(list(filter(lambda m: str(m.status) == "streaming", server.members))),
                        len(list(filter(lambda m: str(m.status) == "offline", server.members)))]

            last_boost = max(server.members, key=lambda m : m.premium_since or server.created_at)
            if last_boost.premium_since is not None:
                boost = f"{last_boost} {discord.utils.format_dt(last_boost.premium_since, style='f')} {discord.utils.format_dt(last_boost.premium_since, style='R')}"
            else:
                boost = "No boosters exist."

            if server.description:
                description = server.description
            else:
                description = "This server doesn't have a description"

            enabled_features = []
            features = set(server.features)
            all_features = {
                'COMMUNITY': 'Community Server',
                'VERIFIED': 'Verified',
                'DISCOVERABLE': 'Discoverable',
                'PARTNERED': 'Partnered',
                'FEATURABLE': 'Featured',
                'COMMERCE': 'Commerce',
                'MONETIZATION_ENABLED': 'Monetization',
                'NEWS': 'News Channels',
                'PREVIEW_ENABLED': 'Preview Enabled',
                'INVITE_SPLASH': 'Invite Splash',
                'VANITY_URL': 'Vanity Invite URL',
                'ANIMATED_ICON': 'Animated Server Icon',
                'BANNER': 'Server Banner',
                'MORE_EMOJI': 'More Emoji',
                'MORE_STICKERS': 'More Stickers',
                'WELCOME_SCREEN_ENABLED': 'Welcome Screen',
                'MEMBER_VERIFICATION_GATE_ENABLED': 'Membership Screening',
                'TICKETED_EVENTS_ENABLED': 'Ticketed Events',
                'VIP_REGIONS': 'VIP Voice Regions',
                'PRIVATE_THREADS': 'Private Threads',
                'THREE_DAY_THREAD_ARCHIVE': '3 Day Thread Archive',
                'SEVEN_DAY_THREAD_ARCHIVE': '1 Week Thread Archive',
            }

            for feature, label in all_features.items():
                if feature in features:
                    enabled_features.append(f"<:greenTick:596576670815879169> {label}")

            features = '\n'.join(enabled_features)

            if features == "":
                features = "This server doesn't have any features."

            if server.premium_tier == 1:
                levelEmoji = "<:Level1_guild:883072977430794240>"
            elif server.premium_tier == 2:
                levelEmoji = "<:Level2_guild:883073003984916491>"
            else:
                levelEmoji = "<:Level3_guild:883073034817245234>"

            verification_level1 = str(server.verification_level)
            verification_level = verification_level1.capitalize()

            if verification_level == "Low":
                verificationEmote = "<:low_verification:883363584464285766>"
            elif verification_level == "Medium":
                verificationEmote = "<:medium_verifiaction:883363595163947120>"
            elif verification_level == "High":
                verificationEmote = "<:high_verifiaction:883363640537915472>"
            elif verification_level == "Highest":
                verificationEmote = "<:highest_verifiaction:883363707332202546>"
            else:
                verificationEmote = "<:none_verifiaction:883363576377659532>"

            if str(server.explicit_content_filter) == "no_role":
                explictContentFilter = "Scan media content from members without a role."
            elif str(server.explicit_content_filter) == "all_members":
                explictContentFilter = "Scan media from all members."
            else:
                explictContentFilter = "Don't scan any media content."
            servers.append(f"""
            <:greyTick:596576672900186113> ID: {server.id}
            :information_source: Description: {description}

            <:members:858326990725709854> Members: {len(server.members)} (:robot: {len(list(filter(lambda m : m.bot, server.members)))})
            :robot: Bots: {len(list(filter(lambda m: m.bot, server.members)))}
            <:owner_crown:845946530452209734> Owner: {server.owner}
            <:members:858326990725709854> Max members: {server.max_members}
            <:bans:878324391958679592> Banned members: {bannedMembers}

            {verificationEmote} Verification level: {verification_level}
            <:channel_nsfw:585783907660857354> Explicit content filter: {explictContentFilter}
            :file_folder: Filesize limit: {pretty_size(server.filesize_limit)}
            Created: {discord.utils.format_dt(server.created_at, style="f")} ({discord.utils.format_dt(server.created_at, style="R")})
            {helpers.get_server_region_emote(server)} Region: {helpers.get_server_region(server)}

            <:status_offline:596576752013279242> Statuses: <:status_online:596576749790429200> {statuses[0]} <:status_idle:596576773488115722> {statuses[1]} <:status_dnd:596576774364856321> {statuses[2]} <:status_streaming:596576747294818305> {statuses[3]} <:status_offline:596576752013279242> {statuses[4]}
            <:text_channel:876503902554578984> Channels: <:text_channel:876503902554578984> {len(server.text_channels)} <:voice:860330111377866774> {len(server.voice_channels)} <:category:882685952999428107> {len(server.categories)} <:stagechannel:824240882793447444> {len(server.stage_channels)} <:threadnew:833432474347372564> {len(server.threads)}
            <:role:876507395839381514> Roles: {len(server.roles)}

            <:emoji_ghost:658538492321595393> Animated emojis: {len([x for x in server.emojis if x.animated])}/{server.emoji_limit}
            <:emoji_ghost:658538492321595393> Non animated emojis: {len([x for x in server.emojis if not x.animated])}/{server.emoji_limit}

            {levelEmoji} Level: {server.premium_tier}
            <:boost:858326699234164756> Boosts: {server.premium_subscription_count}
            <:boost:858326699234164756> Latest booster: {boost}

            Features:
            {features}
            """)


        paginator = ViewMenuPages(source=BotServersEmbedPage(servers, name), clear_reactions_after=True)
        page = await paginator._source.get_page(0)
        kwargs = await paginator._get_kwargs_from_page(page)
        if paginator.build_view():
            paginator.message = await ctx.send(embed=kwargs['embed'],view = paginator.build_view())
        else:
            paginator.message = await ctx.send(embed=kwargs['embed'])
        await paginator.start(ctx)
        
    @commands.command(help="Sends a invite of the bot", alises=['inv', 'invite_me', 'inviteme'])
    async def invite(self, ctx):
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, emoji="<:invite:860644752281436171>", label="Invite me", url="https://discord.com/api/oauth2/authorize?client_id=760179628122964008&permissions=8&scope=bot")
        view.add_item(item=item)

        embed = discord.Embed(title="Click the button to invite me")
        await ctx.send(embed=embed, view=view)
        
    @commands.command(help="Sends you a link where you can vote for the bot", aliases=['topgg', 'top-gg', 'top_gg'])
    async def vote(self, ctx):
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, emoji="<:topgg:870133913102721045>", label="Vote for me", url="https://top.gg/bot/760179628122964008")
        view.add_item(item=item)
        
        embed = discord.Embed(title="Click the button to vote for me")
        await ctx.send(embed=embed, view=view)

    @commands.command(help="Sends the support server of the bot", aliases=['supportserver', 'support_server'])
    async def support(self, ctx):
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, emoji="<:servers:870152102759006208>", label="Join support server", url="https://discord.gg/MrBcA6PZPw")
        view.add_item(item=item)

        embed = discord.Embed(title="Click the button to join the support server")
        await ctx.send(embed=embed, view=view)

    @commands.group(invoke_without_command=True, help="Shows you a list of the bot's prefixes", aliases=['prefix'])
    async def prefixes(self, ctx):
        prefixes = await self.client.get_pre(self.client, ctx.message, raw_prefix=True)
        embed = discord.Embed(title="Here's a list of my prefixes for this server:", description=ctx.me.mention + '\n' + '\n'.join(prefixes))

        return await ctx.send(embed=embed)

    @commands.check_any(commands.has_permissions(manage_guild=True), commands.is_owner())
    @prefixes.command(name="add", help="Adds a prefix to the bot's prefixes", aliases=['a', 'create'])
    async def prefixes_add(self, ctx, new : str):
        old = list(await self.client.get_pre(self.client, ctx.message, raw_prefix=True))

        if len(new) > 50:
            raise errors.TooLongPrefix
            # return await ctx.send("Prefixes can only be up to 50 characters!")

        if len(old) > 30:
            raise errors.TooManyPrefixes
            # return await ctx.send("You can only have 20 prefixes!")

        if new not in old:
            old.append(new)
            await self.client.db.execute(
                "INSERT INTO guilds(guild_id, prefix) VALUES ($1, $2) "
                "ON CONFLICT (guild_id) DO UPDATE SET prefix = $2",
                ctx.guild.id, old)

            self.client.prefixes[ctx.guild.id] = old

            return await ctx.send(f"Successfully added `{new}` to the prefixes.\nMy prefixes are: `{'`, `'.join(old)}`")
        else:
            raise errors.PrefixAlreadyExists
            # return await ctx.send("That's already one of my prefixes!")

    @commands.check_any(commands.has_permissions(manage_guild=True), commands.is_owner())
    @prefixes.command(name="remove", help="Removes a prefix from the bot's prefixes", aliases=['r', 'delete'])
    async def prefixes_remove(self, ctx, prefix : str):
        old = list(await self.client.get_pre(self.client, ctx.message, raw_prefix=True))

        if prefix in old:
            old.remove(prefix)
            await self.client.db.execute(
                "INSERT INTO guilds(guild_id, prefix) VALUES ($1, $2) "
                "ON CONFLICT (guild_id) DO UPDATE SET prefix = $2",
                ctx.guild.id, old)

            self.client.prefixes[ctx.guild.id] = old
            
            if prefix == "sb!":
                # raise errors.UnremoveablePrefix
                return
            else:
                pass

            return await ctx.send(f"Successfully removed `{prefix}`.\nMy prefixes are: `{'`, `'.join(old)}`")
        else:
            raise errors.PrefixDoesntExist
            # return await ctx.send(f"That is not one of my prefixes!")

    @commands.check_any(commands.has_permissions(manage_guild=True), commands.is_owner())
    @prefixes.command(name="clear", help="Clears the bot's prefixes", aliases=['c', 'deleteall'])
    async def prefixes_clear(self, ctx):
        await self.client.db.execute(
            "INSERT INTO guilds(guild_id, prefix) VALUES ($1, $2) "
            "ON CONFLICT (guild_id) DO UPDATE SET prefix = $2",
            ctx.guild.id, None)
        self.client.prefixes[ctx.guild.id] = self.client.PRE
        return await ctx.send("Cleared prefixes!")


    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 120, commands.BucketType.user)
    @helpers.is_sh_server()
    async def chat(self, ctx):
        await ctx.message.delete()
        await ctx.send("▬▬▬.◙.▬▬▬\n" +
                        "═▂▄▄▓▄▄▂\n" +
                        "◢◤ █▀▀████▄▄▄▄◢◤\n" +
                        "█▄ █ █▄ ███▀▀▀▀▀▀▀╬\n" +
                        "◥█████◤\n" +
                        "══╩══╩═\n" +
                        "╬═╬\n" +
                        "╬═╬\n" +
                        "╬═╬\n" +
                        "╬═╬\n" +
                        "╬═╬    just dropped down to ask\n" +
                        "╬═╬\n" +
                        "╬═╬    why chat dead <@&819677363058901033>\n" +
                        "╬═╬ ☻/\n" +
                        "╬═╬/▌\n" +
                        "╬═╬/ \ \n")

    @commands.command(help="Verifies you", hidden=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    # @helpers.is_sh_server()
    async def verify(self, ctx):
        with open("./data/verifyWords.txt", "r") as file:
            allText = file.read()
            wordsList = list(map(str, allText.split()))

        member = ctx.author
        stealth_hangout_role = 'Members'
        classicsmp_role = 'Members'

        correctAnswer = random.choice(wordsList)

        message = await ctx.send(f"Please say `{correctAnswer}` to verify.\nYou have 15 seconds to type the word.")

        def check(m):
            return m.content == correctAnswer and m.channel.id == ctx.channel.id

        try:
            msg = await self.client.wait_for(event='message', check=check, timeout=15)
        except asyncio.TimeoutError:
            await message.delete() # Deletes the bot's message | Please say ... to verify
            await ctx.reply("It's been over 15 seconds, please try again by doing `-verify`", delete_after=5.0) # Replies to the author's message
            await ctx.message.delete() # Deletes the author's message | -verify
        else:
            await message.delete() # Deletes the bot's message | Please say ... to verify
            await msg.delete() # Delete the member's answer
            await ctx.reply("You've successfully verified!", delete_after=5.0)
            await ctx.message.delete() # Deletes the author's message | -verify

            if ctx.guild.id == 799330949686231050: # stealth hangout
                await member.add_roles(discord.utils.get(member.guild.roles, name=stealth_hangout_role))
            elif ctx.guild.id == 882341595528175686: # classicsmp
                await member.add_roles(discord.utils.get(member.guild.roles, name=classicsmp_role))
            else:
                return
                # await member.add_roles(discord.utils.get(member.guild.roles, name=role))

    @commands.command(help="Shows the server address and port of ClassicSMP", aliases=['address', 'classicsmp'])
    @helpers.is_csmp_server()
    async def ip(self, ctx):
        embed = discord.Embed(title="ClassicSMP IP", description="""
```diff
- Java Edition:
+ Server address: play.classic-smp.com

- Bedrock Edition:
+ Server address: play.classic-smp.com
+ Server port: 19132
```
        """)

        await ctx.send(embed=embed)

    @commands.command(aliases=['giveaway_ping', 'ping_giveaway'], help="Pings the Giveaways role", hidden=True)
    @commands.has_role("Staff")
    @commands.cooldown(1, 60, commands.BucketType.user) # Sets the cooldown to 60 seconds for the user executing the command
    async def gping(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"<@&868823472304971817>\n*ping from {ctx.author.mention}*")

    @commands.command(aliases=['qotd_ping', 'ping_qotd'], help="Pings the QOTD role", hidden=True)
    @commands.has_role("Staff")
    @commands.cooldown(1, 60, commands.BucketType.user) # Sets the cooldown to 60 seconds for the user executing the command
    async def qping(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"<@&836281279934496770>\n*ping from {ctx.author.mention}*")

    @commands.command(help="Takes a screenshot of a website", aliases=["ss"])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def screenshot(self, ctx, link):
        URL_REGEX = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        
        if not re.fullmatch(URL_REGEX, link):
            return await ctx.send("Invalid URL! Make sure you put `https://` infront of it.")
        
        else:
            embed=discord.Embed(title=f"{link}")
            embed.set_image(url=f"https://api.popcat.xyz/screenshot?url={link}")
            await ctx.send(embed=embed)

    @commands.command(help="Shows you a list of flags", aliases=['flags'])
    async def flag(self, ctx):
        foo = """🇦🇫
🇦🇽
🇦🇱
🇩🇿
🇦🇸
🇦🇩
🇦🇴
🇦🇮
🇦🇶
🇦🇬
🇦🇷
🇦🇲
🇦🇼
🇦🇺
🇦🇹
🇦🇿
🇧🇸
🇧🇭
🇧🇩
🇧🇧
🇧🇾
🇧🇪
🇧🇿
🇧🇯
🇧🇲
🇧🇹
🇧🇴
🇧🇦
🇧🇼
🇧🇻
🇧🇷
🇮🇴
🇧🇳
🇧🇬
🇧🇫
🇧🇮
🇰🇭
🇨🇲
🇨🇦
🇨🇻
🇧🇶
🇰🇾
🇨🇫
🇹🇩
🇨🇱
🇨🇳
🇨🇽
🇨🇨
🇨🇴
🇰🇲
🇨🇬
🇨🇩
🇨🇰
🇨🇷
🇨🇮
🇭🇷
🇨🇺
🇨🇼
🇨🇾
🇨🇿
🇩🇰
🇩🇯
🇩🇲
🇩🇴
🇪🇨
🇪🇬
🇸🇻
🏴󠁧󠁢󠁥󠁮󠁧󠁿
🇬🇶
🇪🇷
🇪🇪
🇸🇿
🇪🇹
🇫🇰
🇫🇴
🇫🇯
🇫🇮
🇫🇷
🇬🇫
🇵🇫
🇹🇫
🇬🇦
🇬🇲
🇬🇪
🇩🇪
🇬🇭
🇬🇮
🇬🇷
🇬🇱
🇬🇩
🇬🇵
🇬🇺
🇬🇹
🇬🇬
🇬🇳
🇬🇼
🇬🇾
🇭🇹
🇭🇲
🇭🇳
🇭🇰
🇭🇺
🇮🇸
🇮🇳
🇮🇩
🇮🇷
🇮🇶
🇮🇪
🇮🇲
🇮🇱
🇮🇹
🇯🇲
🇯🇵
🇯🇪
🇯🇴
🇰🇿
🇰🇪
🇰🇮
🇰🇵
🇰🇷
🇽🇰
🇰🇼
🇰🇬
🇱🇦
🇱🇻
🇱🇧
🇱🇸
🇱🇷
🇱🇾
🇱🇮
🇱🇹
🇱🇺
🇲🇴
🇲🇬
🇲🇼
🇲🇾
🇲🇻
🇲🇱
🇲🇹
🇲🇭
🇲🇶
🇲🇷
🇲🇺
🇾🇹
🇲🇽
🇫🇲
🇲🇩
🇲🇨
🇲🇳
🇲🇪
🇲🇸
🇲🇦
🇲🇿
🇲🇲
🇳🇦
🇳🇷
🇳🇵
🇳🇱
🇳🇨
🇳🇿
🇳🇮
🇳🇪
🇳🇬
🇳🇺
🇳🇫
🇲🇰
🇲🇵
🇳🇴
🇴🇲
🇵🇰
🇵🇼
🇵🇸
🇵🇦
🇵🇬
🇵🇾
🇵🇪
🇵🇭
🇵🇳
🇵🇱
🇵🇹
🇵🇷
🇶🇦
🇷🇪
🇷🇴
🇷🇺
🇷🇼
🇧🇱
🇸🇭
🇰🇳
🇱🇨
🇲🇫
🇵🇲
🇻🇨
🇼🇸
🇸🇲
🇸🇹
🇸🇦
🏴󠁧󠁢󠁳󠁣󠁴󠁿
🇸🇳
🇷🇸
🇸🇨
🇸🇱
🇸🇬
🇸🇽
🇸🇰
🇸🇮
🇸🇧
🇸🇴
🇿🇦
🇬🇸
🇸🇸
🇪🇸
🇱🇰
🇸🇩
🇸🇷
🇸🇯
🇸🇪
🇨🇭
🇸🇾
🇹🇼
🇹🇯
🇹🇿
🇹🇭
🇹🇱
🇹🇬
🇹🇰
🇹🇴
🇹🇹
🇹🇳
🇹🇷
🇹🇲
🇹🇨
🇹🇻
🇺🇬
🇺🇦
🇦🇪
🇬🇧
🇺🇸
🇺🇲
🇺🇾
🇺🇿
🇻🇺
🇻🇦
🇻🇪
🇻🇳
🇻🇬
🇻🇮
🏴󠁧󠁢󠁷
🇼🇫
🇪🇭
🇾🇪
🇿🇲
🇿🇼"""
        bar = foo.split('\n')
        await ctx.send(f"Here's a list of flags: {', '.join(bar)}")

    @commands.group(aliases=['rtfd'], invoke_without_command=True)
    async def rtfm(self, ctx, *, obj: str = None):
        """Gives you a documentation link for a discord.py entity.
        Events, objects, and functions are all supported through
        a cruddy fuzzy algorithm.
        """
        key = self.transform_rtfm_language_key(ctx, 'latest')
        await self.do_rtfm(ctx, key, obj)

    @rtfm.command(name='jp')
    async def rtfm_jp(self, ctx, *, obj: str = None):
        """Gives you a documentation link for a discord.py entity (Japanese)."""
        await self.do_rtfm(ctx, 'latest-jp', obj)

    @rtfm.command(name='python', aliases=['py'])
    async def rtfm_python(self, ctx, *, obj: str = None):
        """Gives you a documentation link for a Python entity."""
        key = self.transform_rtfm_language_key(ctx, 'python')
        await self.do_rtfm(ctx, key, obj)

    @rtfm.command(name='py-jp', aliases=['py-ja'])
    async def rtfm_python_jp(self, ctx, *, obj: str = None):
        """Gives you a documentation link for a Python entity (Japanese)."""
        await self.do_rtfm(ctx, 'python-jp', obj)

    @rtfm.command(name='master', aliases=['2.0'])
    async def rtfm_master(self, ctx, *, obj: str = None):
        """Gives you a documentation link for a discord.py entity (master branch)"""
        await self.do_rtfm(ctx, 'master', obj)