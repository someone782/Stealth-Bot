import discord
from datetime import datetime
import io
import psutil
import random
import helpers
import os
import textwrap
import unicodedata
import sys
import inspect
import time
import urllib
import time
import pathlib
import pkg_resources
import math
import aiohttp
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType
import threading
from platform import python_version
import asyncio
from afks import afks

from discord.ext import menus
from discord.ext.menus.views import ViewMenuPages

# bytes pretty-printing
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

class ServerEmotesEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=10)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title=f"{self.guild}'s emotes ({len(self.guild.emojis)})", description="\n".join(f'{i+1}. {v}' for i, v in enumerate(entries, start=offset)))
        return embed
    
class ServerMembersEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=20)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title=f"{self.guild}'s members ({len(self.guild.members)})", description="\n".join(f'{i+1}. {v}' for i, v in enumerate(entries, start=offset)))
        return embed
    
class ServerBotsEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=20)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title=f"{self.guild}'s bots ({len(list(filter(lambda m : m.bot, self.ctx.guild.members)))})", description="\n".join(f'{i+1}. {v}' for i, v in enumerate(entries, start=offset)))
        return embed

class ServerRolesEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=20)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title=f"{self.guild}'s roles ({len(menu.ctx.guild.roles)})", description="\n".join(f'{i+1}. {v}' for i, v in enumerate(entries, start=offset)))
        return embed
    
class BotCommandsEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=20)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title=f"{self.ctx.bot.user.name}'s commands ({len(list(self.ctx.bot.commands))})", description="\n".join(f'{i+1}. {v}' for i, v in enumerate(entries, start=offset)))
        return embed
    
class CharInfoEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=20)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title=f"Character information", description="\n".join(entries))
        return embed

def setup(client):
    client.add_cog(Info(client))

class Info(commands.Cog):
    "<:info:888768239889424444> | All informative commands like `serverinfo`, `userinfo` and more!"
    def __init__(self, client):
        self.client = client
        client.session = aiohttp.ClientSession()

    @commands.command(help="Search lyrics of any song", aliases = ['l', 'lyrc', 'lyric'])
    async def lyrics(self, ctx, *, search):
        
        loadingEmbed = discord.Embed(title="Getting lyrics...")
        
        message = await ctx.send(embed=loadingEmbed)
        
        start = time.perf_counter()
        
        song = urllib.parse.quote(search)
        
        async with self.client.session.get(f'https://some-random-api.ml/lyrics?title={song}') as json:
            if not 300 > json.status >= 200:
                return await ctx.send(f'Recieved poor status code of {jsondata.status}')

            jsonData = await json.json()

        error = jsonData.get('error')
        if error:
            raise error

        lyrics = jsonData['lyrics']
        artist = jsonData['author']
        title = jsonData['title']
        thumbnail = jsonData['thumbnail']['genius']
        
        end = time.perf_counter()
        
        ms = (end - start) * 1000
        
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        
        await message.delete()

        for chunk in textwrap.wrap(lyrics, 2048, replace_whitespace=False):
            embed = discord.Embed(title=f"{title} - {artist}", description=chunk, timestamp=discord.utils.utcnow(), color=color)
            embed.set_thumbnail(url=thumbnail)
            embed.set_footer(text=f"{round(ms)}ms{' ' * (9-len(str(round(ms, 3))))}", icon_url=ctx.author.avatar.url)
            
            await ctx.reply(embed=embed)

    @commands.command(help="Shows you information about the member you mentioned", aliases=['ui', 'user', 'member', 'memberinfo'], brief="https://cdn.discordapp.com/attachments/876937268609290300/886407195279884318/userinfo.gif")
    @commands.cooldown(1, 5, BucketType.member)
    async def userinfo(self, ctx, member : discord.Member=None):
        # if member == None:
        #     member = ctx.author
            
        if member == None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                
        fetchedMember = await self.client.fetch_user(member.id)

        if member.bot == True:
            botText = "Yes"
        else:
            botText = "No"

        if member.pending == True:
            pendingText = "Yes"
        else:
            pendingText = "No"

        if member.premium_since == None:
            premiumText = "Not boosting"
        else:
            premiumText = f"{discord.utils.format_dt(member.premium_since, style='f')} ({discord.utils.format_dt(member.premium_since, style='R')})"

        if str(member.status).title() == "Online":
            statusEmote = "<:status_online:596576749790429200>"
        elif str(member.status).title() == "Idle":
            statusEmote = "<:status_idle:596576773488115722>"
        elif str(member.status).title() == "Dnd":
            statusEmote = "<:status_dnd:596576774364856321>"
        elif str(member.status).title() == "Streaming":
            statusEmote = "<:status_streaming:596576747294818305>"
        else:
            statusEmote = "<:status_offline:596576752013279242>"

        roles = ""
        for role in member.roles:
            if role is ctx.guild.default_role: continue
            roles = f"{roles} {role.mention}"
        if roles != "":
            roles = f"{roles}"

        badges = helpers.get_member_badges(member)
        if badges:
            badges = f"{badges}"
        else:
            badges = ''

        perms = helpers.get_perms(member.guild_permissions)
        if perms:
            perms = f"{' **|** '.join(perms)}"
        else:
            perms = ''

        if member.avatar.is_animated() == True:
            avatar = f"[PNG]({member.avatar.replace(format='png', size=2048).url}) **|** [JPG]({member.avatar.replace(format='jpg', size=2048).url}) **|** [JPEG]({member.avatar.replace(format='jpeg', size=2048).url}) **|** [WEBP]({member.avatar.replace(format='webp', size=2048).url}) **|** [GIF]({member.avatar.replace(format='gif', size=2048).url})"
        else:
            avatar = f"[PNG]({member.avatar.replace(format='png', size=2048).url}) **|** [JPG]({member.avatar.replace(format='jpg', size=2048).url}) **|** [JPEG]({member.avatar.replace(format='jpeg', size=2048).url}) **|** [WEBP]({member.avatar.replace(format='webp', size=2048).url})"

        fetchedMember = await self.client.fetch_user(member.id)

        if fetchedMember.banner:
            if fetchedMember.banner.is_animated() == True:
                avatar = f"[PNG]({fetchedMember.banner.replace(format='png', size=2048).url}) **|** [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) **|** [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) **|** [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url}) **|** [GIF]({fetchedMember.banner.replace(format='gif', size=2048).url})"
            else:
                avatar = f"[PNG]({fetchedMember.avatar.replace(format='png', size=2048).url}) **|** [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) **|** [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) **|** [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url})"
        else:
            banner = "No banner found"

        guild = ctx.guild

        desktopStatus = ":desktop: <:redTick:596576672149667840>"
        webStatus = ":globe_with_meridians: <:redTick:596576672149667840>"
        mobileStatus = ":mobile_phone:  <:redTick:596576672149667840>"

        if str(member.desktop_status) == "online" or str(member.desktop_status) == "idle" or str(member.desktop_status) == "dnd" or str(member.desktop_status) == "streaming":
            desktopStatus = ":desktop: <:greenTick:596576670815879169>"

        if str(member.web_status) == "online" or str(member.web_status) == "idle" or str(member.web_status) == "dnd" or str(member.web_status) == "streaming":
            webStatus = ":globe_with_meridians: <:greenTick:596576670815879169>"

        if str(member.mobile_status) == "online" or str(member.mobile_status) == "idle" or str(member.mobile_status) == "dnd" or str(member.mobile_status) == "streaming":
            mobileStatus = ":mobile_phone: <:greenTick:596576670815879169>"

        if member.id in afks.keys():
            afkStatus = "Yes"
        else:
            afkStatus = "No"

        # copied code :troll: \/ \/ \/

        joined = sorted(ctx.guild.members, key=lambda mem: mem.joined_at)
        pos = joined.index(member)
        positions = []
        for i in range(-3, 4):
            line_pos = pos + i
            if line_pos < 0:
                continue
            if line_pos >= len(joined):
                break
            positions.append("{0:<4}{1}{2:<20}".format(str(line_pos + 1) + ".", " " * 4 + (">" if joined[line_pos] == member else " "), str(joined[line_pos])))
        join_seq = "{}".format("\n".join(positions))

        members = [*sorted(ctx.guild.members, key=lambda m: m.joined_at)]
        x = members.index(ctx.author)
        join_pos = "\n".join(map(str, members[x - 3: x + 3]))

        # copied code :troll: /\ /\ /\


    # {sorted(ctx.guild.members, key=lambda member : member.joined_at).index(member) + 1}

        acknowledgments = "None"
        if member.id == 564890536947875868:
            acknowledgments = ":crown: Owner"
        elif member.id == 349373972103561218:
            acknowledgments = "Helped with a lot of stuff"
        elif member.id == 636292554416979979:
            acknowledgments = "retard"
            
        nickname = member.nick
        if member.nick == None:
            nickname = f"{member.name} (No nickname)"


        embed = discord.Embed(title=f"{member}", url=f"https://discord.com/users/{member.id}", description=f"""
<:nickname:876507754917929020> Nickname: {nickname}
:hash: Discriminator:  #{member.discriminator}
Mention: {member.mention}
<:greyTick:596576672900186113> ID: {member.id}

:robot: Bot?: {botText}
Pending verification?: {pendingText}
AFK?: {afkStatus}
Avatar url: {avatar}
Banner url: {banner}

<a:nitro_wumpus:857636144875175936> Boosting: {premiumText}
<:invite:860644752281436171> Created: {discord.utils.format_dt(member.created_at, style="f")} ({discord.utils.format_dt(member.created_at, style="R")})
<:member_join:596576726163914752> Joined: {discord.utils.format_dt(member.joined_at, style="f")} ({discord.utils.format_dt(member.joined_at, style="R")})
<:moved:848312880666640394> Join position:
```yaml
{join_seq}
```
Mutual guilds: {len(member.mutual_guilds)}

{statusEmote} Current status: {str(member.status).title()}
:video_game: Current activity: {str(member.activity.type).split('.')[-1].title() if member.activity else 'Not playing'} {member.activity.name if member.activity else ''}
<:discord:877926570512236564> Client: {desktopStatus} **|** {webStatus} **|** {mobileStatus}

<:role:876507395839381514> Top Role: {member.top_role.mention}
<:role:876507395839381514> Roles: {roles}
<:store_tag:860644620857507901> Staff permissions: {perms}
<:store_tag:860644620857507901> Badges: {badges}
Acknowledgments: {acknowledgments}

:rainbow: Color: {member.color}
:rainbow: Accent color: {fetchedMember.accent_color}
        """)
        embed.set_thumbnail(url=member.avatar.url)

        await ctx.send(embed=embed)


    @commands.command(help="Shows you information about the server", aliases=['si', 'guild', 'guildinfo'])
    @commands.cooldown(1, 5, BucketType.member)
    async def serverinfo(self, ctx, id : int=None):
        if id:
            server = self.client.get_guild(id)
            if not server:
                return await ctx.send("I couldn't find that server. Make sure the ID you entered was correct.")
        else:
            server = ctx.guild

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

        embed = discord.Embed(title=f"{server}", description=f"""
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

        if server.banner:
            embed.set_image(url=server.banner)


        if server.icon:
            embed.set_thumbnail(url=server.icon)

        await ctx.send(embed=embed)
        
    @commands.command(help="Shows information about a emoji", aliases=['ei', 'emoteinfo', 'emoinfo', 'eminfo', 'emojinfo', 'einfo'])
    async def emojiinfo(self, ctx, emoji : discord.PartialEmoji):
        url = f"{emoji.url}"
        animated = "No"
        
        if emoji.animated == True:
            animated = "Yes"

        embed = discord.Embed(title=f"{emoji.name}", description=f"""
Name: {emoji.name}
<:greyTick:860644729933791283> ID: {emoji.id}

Created at: {discord.utils.format_dt(emoji.created_at, style="f")} ({discord.utils.format_dt(emoji.created_at, style="R")})
:link: Link: [Click here]({emoji.url})

<:emoji_ghost:658538492321595393> Animated?: {animated}
                              """)
        embed.set_thumbnail(url=emoji.url)
        
        await ctx.send(embed=embed)
        

    @commands.command(help="Shows information about the bot", aliases=['bi'])
    async def botinfo(self, ctx):
        prefixes = await self.client.get_pre(self.client, ctx.message, raw_prefix=True)
        text = ctx.me.mention + '\n' + '\n'.join(prefixes)
        p = pathlib.Path('./')
        cm = cr = fn = cl = ls = fc = 0
        for f in p.rglob('*.py'):
            if str(f).startswith("venv"):
                continue
            fc += 1
            with f.open() as of:
                for l in of.readlines():
                    l = l.strip()
                    if l.startswith('class'):
                        cl += 1
                    if l.startswith('def'):
                        fn += 1
                    if l.startswith('async def'):
                        cr += 1
                    if '#' in l:
                        cm += 1
                    ls += 1

        text_channels = len([channel for channel in self.client.get_all_channels() if isinstance(channel, discord.TextChannel)])
        voice_channels = len([channel for channel in self.client.get_all_channels() if isinstance(channel, discord.VoiceChannel)])
        categories = len([channel for channel in self.client.get_all_channels() if isinstance(channel, discord.CategoryChannel)])
        stage_channels = len([channel for channel in self.client.get_all_channels() if isinstance(channel, discord.StageChannel)])
        threads = channels = len([channel for channel in self.client.get_all_channels() if isinstance(channel, discord.Thread)])

        embed = discord.Embed(title=f"{self.client.user.name}", description=f"""
<:members:858326990725709854> Members: {len(self.client.users)} (:robot: {len(list(filter(lambda m : m.bot, self.client.users)))})
<:servers:870152102759006208> Servers: {len(self.client.guilds)}
<:text_channel:876503902554578984> Channels: <:text_channel:876503902554578984> {text_channels} <:voice:860330111377866774> {voice_channels} <:category:882685952999428107> {categories} <:stagechannel:824240882793447444> {stage_channels} <:threadnew:833432474347372564> {threads}

Prefixes:
{text}
Messages seen: {self.client.messages} ({self.client.edited_messages} edited)

:file_folder: Files: {fc}
Lines: {ls:,}
Classes: {cl}
Functions: {fn}
Coroutine: {cr}
:hash: Comments: {cm:,}

Enhanced-dpy version: 
Python version: 

        """)
        embed.set_thumbnail(url=self.client.user.avatar.url)

        await ctx.send(embed=embed)

    @commands.command(help="Shows a list of commands this bot has", aliases=['commands', 'command', 'cmds', 'commandslist', 'cmdslist', 'commands_list', 'cmds_list', 'commandlist', 'cmdlist', 'command_list', 'cmd_list'])
    async def _commands(self, ctx):
        botCommands = self.client.commands
        commands = []

        for command in botCommands:

            commands.append(f"{command.name} **|** {command.mention} **|** `{command.id}`")
            
        commands = [sub.replace('hentai', '||hentai||') for sub in commands]

        paginator = ViewMenuPages(source=ServerBotsEmbedPage(commands, guild), clear_reactions_after=True)
        page = await paginator._source.get_page(0)
        kwargs = await paginator._get_kwargs_from_page(page)
        if paginator.build_view():
            paginator.message = await ctx.send(embed=kwargs['embed'],view = paginator.build_view())
        else:
            paginator.message = await ctx.send(embed=kwargs['embed'])
        await paginator.start(ctx)

    @commands.command(help="Shows you a list of emotes from this server", aliases=['emojilist', 'emote_list', 'emoji_list', 'emotes', 'emojis'])
    async def emotelist(self, ctx, id : int=None):
        if id:
            guild = self.client.get_guild(id)
            if not guild:
                return await ctx.send("I couldn't find that server. Make sure the ID you entered was correct.")
        else:
            guild = ctx.guild

        guildEmotes = guild.emojis
        emotes = []

        for emoji in guildEmotes:

          if emoji.animated:
             emotes.append(f"<a:{emoji.name}:{emoji.id}> **|** {emoji.name} **|** [`<a:{emoji.name}:{emoji.id}>`]({emoji.url})")

          if not emoji.animated:
              emotes.append(f"<:{emoji.name}:{emoji.id}> **|** {emoji.name} **|** [`<:{emoji.name}:{emoji.id}>`]({emoji.url})")

        paginator = ViewMenuPages(source=ServerEmotesEmbedPage(emotes,guild), clear_reactions_after=True)
        page = await paginator._source.get_page(0)
        kwargs = await paginator._get_kwargs_from_page(page)
        if paginator.build_view():
            paginator.message = await ctx.send(embed=kwargs['embed'],view = paginator.build_view())
        else:
            paginator.message = await ctx.send(embed=kwargs['embed'])
        await paginator.start(ctx)
        
    @commands.command(help="Shows you a list of members from this server", aliases=['member_list', 'memlist', 'mem_list'])
    async def memberlist(self, ctx, id : int=None):
        if id:
            guild = self.client.get_guild(id)
            if not guild:
                return await ctx.send("I couldn't find that server. Make sure the ID you entered was correct.")
        else:
            guild = ctx.guild

        guildMembers = guild.members
        members = []

        for member in guildMembers:

            members.append(f"{member.name} **|** {member.mention} **|** `{member.id}`")

        paginator = ViewMenuPages(source=ServerMembersEmbedPage(members, guild), clear_reactions_after=True)
        page = await paginator._source.get_page(0)
        kwargs = await paginator._get_kwargs_from_page(page)
        if paginator.build_view():
            paginator.message = await ctx.send(embed=kwargs['embed'],view = paginator.build_view())
        else:
            paginator.message = await ctx.send(embed=kwargs['embed'])
        await paginator.start(ctx)
        
    @commands.command(help="Shows you a list of bots from this server", aliases=['bot_list', 'bolist', 'bo_list', 'bots', 'bot'])
    async def botlist(self, ctx, id : int=None):
        if id:
            guild = self.client.get_guild(id)
            if not guild:
                return await ctx.send("I couldn't find that server. Make sure the ID you entered was correct.")
        else:
            guild = ctx.guild

        guildBots = list(filter(lambda m : m.bot, server.members))
        bots = []

        for bot in guildBots:

            bots.append(f"{bot.name} **|** {bot.mention} **|** `{bot.id}`")

        paginator = ViewMenuPages(source=ServerBotsEmbedPage(bots, guild), clear_reactions_after=True)
        page = await paginator._source.get_page(0)
        kwargs = await paginator._get_kwargs_from_page(page)
        if paginator.build_view():
            paginator.message = await ctx.send(embed=kwargs['embed'],view = paginator.build_view())
        else:
            paginator.message = await ctx.send(embed=kwargs['embed'])
        await paginator.start(ctx)
        
    @commands.command(help="Shows you a list of roles from this server", aliases=['role_list', 'rolist', 'ro_list', 'roles', 'role'])
    async def rolelist(self, ctx, id : int=None):
        if id:
            guild = self.client.get_guild(id)
            if not guild:
                return await ctx.send("I couldn't find that server. Make sure the ID you entered was correct.")
        else:
            guild = ctx.guild

        guildRoles = server.roles
        roles = []

        for role in guildRoles:

            roles.append(f"{role.name} **|** {role.mention} **|** `{role.id}`")

        paginator = ViewMenuPages(source=ServerBotsEmbedPage(roles, guild), clear_reactions_after=True)
        page = await paginator._source.get_page(0)
        kwargs = await paginator._get_kwargs_from_page(page)
        if paginator.build_view():
            paginator.message = await ctx.send(embed=kwargs['embed'],view = paginator.build_view())
        else:
            paginator.message = await ctx.send(embed=kwargs['embed'])
        await paginator.start(ctx)

    @commands.command(help="Shows information about the channel", aliases=['ci', 'channel'])
    async def channelinfo(self, ctx, channel : discord.TextChannel=None):
        if channel == None:
            channel = ctx.channel

        pins = await channel.pins()

        embed = discord.Embed(title=f"{channel}", description=f"""
Mention: {channel.mention}
ID: {channel.id}
Topic: {channel.topic}

Pins: {len(pins)}
Position: {channel.position}
Server: {channel.guild}
Slowmode: {channel.slowmode_delay}
Creation date: {discord.utils.format_dt(channel.created_at, style="f")} ({discord.utils.format_dt(channel.created_at, style="R")})
        """)

        await ctx.send(embed=embed)

    @commands.command(help="Shows the avatar of the member you mentioned", aliases=['av'])
    @commands.cooldown(1, 5, BucketType.member)
    async def avatar(self, ctx, member : discord.Member=None):
        errorMessage = f"{member} doesnt have a avatar."
        if member == None:
            member = ctx.author
            errorMessage = "You don't have a avatar."
            
            
        if member.avatar:
            
            if member.avatar.is_animated() == True:
                text1 = f"[PNG]({member.avatar.replace(format='png', size=2048).url}) | [JPG]({member.avatar.replace(format='jpg', size=2048).url}) | [JPEG]({member.avatar.replace(format='jpeg', size=2048).url}) | [WEBP]({member.avatar.replace(format='webp', size=2048).url}) | [GIF]({member.avatar.replace(format='gif', size=2048).url})"
                text = text1.replace("cdn.discordapp.com", "media.discordapp.net")
                
            else:
                text1 = f"[PNG]({member.avatar.replace(format='png', size=2048).url}) | [JPG]({member.avatar.replace(format='jpg', size=2048).url}) | [JPEG]({member.avatar.replace(format='jpeg', size=2048).url}) | [WEBP]({member.avatar.replace(format='webp', size=2048).url})"
                text = text1.replace("cdn.discordapp.com", "media.discordapp.net")
                
            embed=discord.Embed(title=f"{member}'s avatar", description=f"{text}")
            url1 = member.avatar.url
            url = url1.replace("cdn.discordapp.com", "media.discordapp.net")
            embed.set_image(url=url)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{errorMessage}")

    @commands.command(help="Shows the banner of the member you mentioned", aliases=['bn'])
    @commands.cooldown(1, 5, BucketType.member)
    async def banner(self, ctx, member : discord.Member=None):
        errorMessage = f"{member} doesn't have a banner."
        if member == None or member == ctx.author:
            member = ctx.author
            errorMessage = "You don't have a banner"

        fetchedMember = await self.client.fetch_user(member.id)

        if fetchedMember.banner:
            
            if fetchedMember.banner.is_animated() == True:
                text1 = f"[PNG]({fetchedMember.banner.replace(format='png', size=2048).url}) | [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) | [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) | [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url}) | [GIF]({fetchedMember.banner.replace(format='gif', size=2048).url})"
                text = text1.replace("cdn.discordapp.com", "media.discordapp.net")
                
            else:
                text1 = f"[PNG]({fetchedMember.avatar.replace(format='png', size=2048).url}) | [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) | [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) | [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url})"
                text = text1.replace("cdn.discordapp.com", "media.discordapp.net")
                
            embed=discord.Embed(title=f"{member}'s avatar", description=f"{text}")
            url1 = fetchedMember.banner.url
            url = url1.replace("cdn.discordapp.com", "media.discordapp.net")
            embed.set_image(url=url)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{errorMessage}")

    @commands.command(help="Shows you the bot's latency")
    @commands.cooldown(1, 5, BucketType.member)
    async def ping(self, ctx):
        pings = []
        number = 0

        typings = time.monotonic()
        await ctx.trigger_typing()
        typinge = time.monotonic()
        typingms = (typinge - typings) * 1000
        pings.append(typingms)

        start = time.perf_counter()
        message = await ctx.send("Getting ping...")
        end = time.perf_counter()
        messagems = (end - start) * 1000
        pings.append(messagems)

        discords = time.monotonic()
        url = "https://discordapp.com/"
        async with self.client.session.get(url) as resp:
            if resp.status == 200:
                discorde = time.monotonic()
                discordms = (discorde - discords) * 1000
                pings.append(discordms)
            else:
                discordms = 0

        latencyms = self.client.latency * 1000
        pings.append(latencyms)

        pstart = time.perf_counter()
        await self.client.db.fetch("SELECT 1")
        pend = time.perf_counter()
        psqlms = (pend - pstart) * 1000
        pings.append(psqlms)

        for ms in pings:
            number += ms
        average = number / len(pings)

        websocket_latency = f"{round(latencyms)}ms{' ' * (9-len(str(round(latencyms, 3))))}"
        typing_latency = f"{round(typingms)}ms{' ' * (9-len(str(round(typingms, 3))))}"
        message_latency = f"{round(messagems)}ms{' ' * (9-len(str(round(messagems, 3))))}"
        discord_latency = f"{round(discordms)}ms{' ' * (9-len(str(round(discordms, 3))))}"
        database_latency = f"{round(psqlms)}ms{' ' * (9-len(str(round(psqlms, 3))))}"
        average_latency = f"{round(average)}ms{' ' * (9-len(str(round(average, 3))))}"

        embed = discord.Embed(title="Pong!")
        embed.add_field(name=":globe_with_meridians: Websocket latency", value=f"{websocket_latency}")
        embed.add_field(name="<a:typing:597589448607399949> Typing latency", value=f"{typing_latency}")
        embed.add_field(name=":speech_balloon: Message latency", value=f"{message_latency}")
        embed.add_field(name="<:discord:877926570512236564> Discord latency", value=f"{discord_latency}")
        embed.add_field(name="<:psql:871758815345901619> Database latency", value=f"{database_latency}")
        embed.add_field(name=":infinity: Average latency", value=f"{average_latency}")

        await message.edit(content="Received ping!", embed=embed)

    @commands.command(help="Shows you the uptime of the bot", aliases=['up'])
    async def uptime(self, ctx):
        delta_uptime = discord.utils.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        text = f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds"

        embed = discord.Embed(title=f"I've been online for {text}\n{discord.utils.format_dt(self.client.launch_time, style='f')} ({discord.utils.format_dt(self.client.launch_time, style='R')})")

        await ctx.send(embed=embed)

    @commands.command(help="Shows how many servers the bot is in", aliases=['server'])
    async def servers(self, ctx):
        embed = discord.Embed(title=f"I' in `{self.client.guilds}` servers.")

        await ctx.send(embed=embed)

    @commands.command(help="Shows how many messages the bot has seen", aliases=['msg', 'msgs', 'message'])
    async def messages(self, ctx):
        embed = discord.Embed(title=f"I've a total of `{self.client.messages}` messages and `{self.client.edited_messages}` edits.")
        
        await ctx.send(embed=embed)

    @commands.command()
    async def snipe(self, ctx):
        embed = discord.Embed(title="Sniped message", description=f"Message: {self.client.last_message}\nAuthor: {self.client.last_message_author} **|** {self.client.last_message_author.id}")

        await ctx.send(embed=embed)

    @commands.command(help="Sends a suggestion", aliases=['bot_suggestion', 'suggestion', 'make_suggestion', 'botsuggestion', 'makesuggestion'])
    async def suggest(self, ctx, *, suggestion):
        if len(suggestion) > 750:
            return await ctx.send("Your suggestion exceeded the 750-character limit.")
        
        else:
            embed = discord.Embed(title="Bot suggestion", description=f"""
Suggestion by: {ctx.author} | {ctx.author.name} | {ctx.author.id}

Suggestion from server: {ctx.guild} | {ctx.guild.id}

Suggestion from channel: {ctx.channel} | {ctx.channel.name} | {ctx.channel.id}

Suggestion: {suggestion}
            """)
            channel = self.client.get_channel(879786064473129033)
            await channel.send(embed=embed)
            
            await ctx.send("Your suggestion has been sent! It will be reviewed by Ender2K89 soon.")

    @commands.command(help="Shows you information about a character", aliases=['characterinfo', 'character_info', 'char_info'])
    @commands.cooldown(1, 5, BucketType.member)
    async def charinfo(self, ctx, *, characters: str):
        def to_string(c):
            digit = f'{ord(c):x}'
            name = unicodedata.name(c, 'Name not found.')
            return f'`\\U{digit:>08}`: {name} - **{c}** \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{digit}>'
        msg = '\n'.join(map(to_string, characters))

        menu = menus.MenuPages(CharInfoEmbedPage(msg.split("\n"), per_page=20), delete_message_after=True)
        
        await menu.start(ctx)

    @commands.command(help="Shows you who helped with the making of this bot", aliases=['credit'])
    async def credits(self, ctx):
        embed = discord.Embed(title="Credits", description="""
```yaml
Owner: Ender2K89#9999
Helped with a lot: LeoCx1000#9999
Main help command page inspired by: Charles#5244
Made music cog: DaPandaOfficial🐼#5684
A lot of command ideas: Vicente0670 YT#0670
A lot of command ideas too: ROLEX#0009
Tested verify command: Eiiknostv#2016
```
        """)

        await ctx.send(embed=embed)

    @commands.command(help="Shows the current time", aliases=['date'])
    async def time(self, ctx):
        embed = discord.Embed(title=f"The current time is {discord.utils.format_dt(discord.utils.utcnow(), style='T')}")
        
        await ctx.send(embed=embed)

    @commands.command()
    async def afk(self, ctx, *, reason=None):
        member = ctx.author
        if reason == None:
            reason = "No reason provided."

        if member.id in afks.keys():
            afks.pop(member.id)
        else:
            try:
                await member.edit(nick=f"[AFK] {member.display_name}")
            except:
                pass

        afks[member.id] = reason

        await ctx.send(f"{member} went afk cause `{reason}`")

    @commands.command(help="Sends the source code of the bot/a command")
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def source(self, ctx, *, command : str=None):
        prefix = ctx.clean_prefix
        source_url = 'https://github.com/Ender2K89/Stealth-Bot'

        if command is None:
            embed = discord.Embed(title=f"Click here for the source code of this bot", url=f"{source_url}")

            view = discord.ui.View()
            style = discord.ButtonStyle.gray
            item = discord.ui.Button(style=style, emoji="<:github:744345792172654643>", label="Source code", url=f"{source_url}")
            view.add_item(item=item)

            return await ctx.send(embed=embed, view=view)

        if command == 'help':
            src = type(self.client.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)

        else:
            obj = self.client.get_command(command.replace('.', ' '))

            if obj is None:
                embed = discord.Embed(title=f"Click here for the source code of this bot", description="I couldn't find that command", url=f"{source_url}")

                view = discord.ui.View()
                style = discord.ButtonStyle.gray
                item = discord.ui.Button(style=style, emoji="<:github:744345792172654643>", label="Source code", url=f"{source_url}")
                view.add_item(item=item)
                return await ctx.send(embed=embed, view=view)

            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)

        if not module.startswith('discord'):
            location = os.path.relpath(filename).replace('\\', '/')

        else:
            location = module.replace('.', '/') + '.py'
            source_url = 'https://github.com/Rapptz/discord.py'
            branch = 'master'

        final_url = f'{source_url}/tree/main/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}'
        embed = discord.Embed(title=f"Click here for the source code of the `{prefix}{command}` command", url=f"{final_url}")
        embed.set_footer(text=f"{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}")

        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, emoji="<:github:744345792172654643>", label="Source code", url=f"{final_url}")
        view.add_item(item=item)

        await ctx.send(embed=embed, view=view)
