import discord
from datetime import datetime
import io
import psutil
import helpers.helpers as helpers
import os
import textwrap
import unicodedata
import sys
import inspect
import typing
import time
import urllib
import time
import random
import pathlib
import contextlib
import pkg_resources
import math
import aiohttp
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType
import threading
from platform import python_version
import asyncio
from discord.ext.menus.views import ViewMenuPages
import re
import zlib
from typing import Any, Dict, List, Optional, Union

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


def reading_recursive(root: str, /) -> int:
    for x in os.listdir(root):
        if os.path.isdir(x):
            yield from reading_recursive(root + "/" + x)
        else:
            if x.endswith((".py", ".c")):
                with open(f"{root}/{x}") as r:
                    yield len(r.readlines())

def count_python(root: str) -> int:
    return sum(reading_recursive(root))

class Dropdown(discord.ui.Select):
    def __init__(self, ctx, view):
        self.ctx = ctx
        self.view_ = view
        if ctx.channel.is_nsfw() == True:
            options = [
                discord.SelectOption(label="Info", description="All informative commands like serverinfo, userinfo and more!", emoji="<:info:888768239889424444>"),
                discord.SelectOption(label="Fun", description="Fun commands like -meme, -hug and more", emoji="⚽"),
                discord.SelectOption(label="Misc", description="Miscellaneous commands", emoji="⚙️"),
                discord.SelectOption(label="Mod", description="Moderation commands", emoji="<:staff:858326975869485077>"),
                discord.SelectOption(label="Games", description="Commands used to play games when you're bored!", emoji="🎮"),
                discord.SelectOption(label="Music", description="Commands used to play/control music", emoji="<a:music:888778105844563988>"),
                discord.SelectOption(label="NSFW", description="NSFW commands, type \"gif\" as the type and it'll be animated", emoji="🔞"),
                discord.SelectOption(label="Owner", description="Commands that only the developer of this bot can use", emoji="<:owner_crown:845946530452209734>"),
                discord.SelectOption(label="Custom", description="Commands that are made by members who won a giveaway called \"Custom command for Stealth Bot\"", emoji="🎉"),
                discord.SelectOption(label="Images", description="Commands that show you images?...", emoji="🖼️")]
        else: # i know this is a terrible way of doing it, i don't care.
            options = [
                discord.SelectOption(label="Info", description="All informative commands like serverinfo, userinfo and more!", emoji="<:info:888768239889424444>"),
                discord.SelectOption(label="Fun", description="Fun commands like -meme, -hug and more", emoji="⚽"),
                discord.SelectOption(label="Misc", description="Miscellaneous commands", emoji="⚙️"),
                discord.SelectOption(label="Mod", description="Moderation commands", emoji="<:staff:858326975869485077>"),
                discord.SelectOption(label="Games", description="Commands used to play games when you're bored!", emoji="🎮"),
                discord.SelectOption(label="Music", description="Commands used to play/control music", emoji="<a:music:888778105844563988>"),
                discord.SelectOption(label="Owner", description="Commands that only the developer of this bot can use", emoji="<:owner_crown:845946530452209734>"),
                discord.SelectOption(label="Custom", description="Commands that are made by members who won a giveaway called \"Custom command for Stealth Bot\"", emoji="🎉"),
                discord.SelectOption(label="Images", description="Commands that show you images?...", emoji="🖼️")]

        super().__init__(placeholder='Select a category...', min_values=1, max_values=1, options=options)
        
    def get_minimal_command_signature(self, command):
        return "%s%s %s" % (self.ctx.clean_prefix, command.qualified_name, command.signature)

    def get_command_name(self, command):
        return "%s" % (command.qualified_name)

    async def callback(self, interaction: discord.Interaction):
        cog = self.ctx.bot.get_cog(self.values[0])
        
        if cog.qualified_name.lower() == "nsfw" and self.ctx.channel.is_nsfw() == False: # you forgor 'self'
            raise commands.NSFWChannelRequired(self.ctx.channel)
        
        entries = cog.get_commands()
        command_signatures = [self.get_minimal_command_signature(c) for c in entries]
        if command_signatures:
            val = "\n".join(command_signatures)
            
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)

        embed = discord.Embed(title=f"Help - {cog.qualified_name}", description=f"""
Total commands: {len(cog.get_commands())}
Commands usable by you (in this server): 
```diff
- <> = required argument
- [] = optional argument
+ Type help [command] for help on a command
```
                            """, timestamp=discord.utils.utcnow(), color=color)
        embed.add_field(name=f"Category: {cog.qualified_name}", value=f"""
{cog.description.split('|' )[0]} {cog.description.split('| ')[1]}
```yaml
{val}
```
                        """)
        
        await interaction.message.edit(embed=embed, view = self.view_) #you need to update the view to listen to further interaction

class VoteButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(emoji="<:dbl:757235965629825084>", label='top.gg', url="https://top.gg/bot/760179628122964008"))
        self.add_item(discord.ui.Button(emoji="<:botsgg:895688440547520512>", label='bots.gg', url="https://discord.bots.gg/bots/760179628122964008"))

class Stuff(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.add_item(Dropdown(ctx, self))
        url = "https://discord.com/api/oauth2/authorize?client_id=760179628122964008&permissions=8&scope=bot"
        self.add_item(discord.ui.Button(emoji="<:invite:895688440639799347>", label='Invite me', url=url))
        self.add_item(discord.ui.Button(emoji="<:github:895688440492986389>", label='Source code', url="https://github.com/Ender2K89/Stealth-Bot"))

    @discord.ui.button(label="Vote", emoji="<:dbl:757235965629825084>", style=discord.ButtonStyle.gray)
    async def vote(self, button : discord.ui.Button, interaction : discord.Interaction):
        embed=discord.Embed(title="Vote for me")
        await interaction.response.send_message(embed=embed, ephemeral=True, view=VoteButtons())
        
    @discord.ui.button(label="Delete", emoji="🗑️", style=discord.ButtonStyle.red)
    async def delete(self, button : discord.ui.Button, interaction : discord.Interaction):
        await interaction.message.delete()
        
    async def interaction_check(self, interaction: discord.Interaction):
            if not interaction.user == self.ctx.author:
                colors = [0x910023, 0xA523FF]
                color = random.choice(colors)
                embed = discord.Embed(description="This isn't your menu.", timestamp=discord.utils.utcnow(), color=color)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                #return False is not need of that cuz we can just return interaction.user == self.ctx.author
            return interaction.user == self.ctx.author
            # else:
            #     self.stop() # self.stop() would stop listening to the components after one interaction 
            #     return True
            
    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Select):
                item.placeholder = "Command disabled due to timeout."
            item.disabled = True
            
        await self.message.edit(view=self)
    

class MyHelp(commands.HelpCommand):
    def get_minimal_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    def get_command_name(self, command):
        return '%s' % (command.qualified_name)

    async def send_bot_help(self, mapping):
        ctx = self.context
        # prefix = self.context.clean_prefix
        prefixes = await self.context.bot.get_pre(self.context.bot, ctx.message, raw_prefix=True)
        prefix = prefixes[0]
        prefixes = ctx.me.mention + ', ' + ', '.join(prefixes)

        delta_uptime = discord.utils.utcnow() - self.context.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        uptime = f"{days}:{hours}:{minutes}:{seconds}"

        if len(prefixes) > 30:
            prefixes = f"[Hover over for a list of prefixes]({ctx.message.jump_url} '{prefixes}')"
        
        with open('./data/news.txt') as f:
            newsFileContext = f.read()
            new1 = f"{newsFileContext}"
            news = new1.replace("%%PREFIX%%", f"{prefix}")
            
        embed = discord.Embed(title="Help", description=f"""
Prefixes: {prefixes}
Total commands: `{len(list(self.context.bot.commands))}`
Commands usable by you (in this server): `{len(await self.filter_commands(list(self.context.bot.commands), sort=True))}`
Written with `{count_python('.'):,}` lines
Uptime: {uptime}
```diff
+ Type {prefix}help [command/category] for help on a command/category
- <> = required argument
- [] = optional argument
```
                              """)

        allcogs = []
        cogindex = []
        ignored_cogs = ['help', 'Jishaku', 'events']
        iter = 1
        for cog, commands in mapping.items():
            if cog is None or cog.qualified_name in ignored_cogs: continue
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_name(c) for c in filtered]
            if command_signatures:
                num = f"{iter}\U0000fe0f\U000020e3" if iter < 10 else "\U0001f51f"
                cogindex.append(cog.qualified_name)
                allcogs.append(f"{cog.description.split('|')[0]} `{prefix}help {cog.qualified_name}`")
                iter+=1
        nl = '\n'
        embed.add_field(name=f"<:category:895688440220356669>  __**Available categories**__ **[{len(allcogs)}]**", value=f"""
{nl.join(allcogs)}
        """)

        embed.add_field(name=":loudspeaker: __**Latest News**__ - **<t:1631999898:d> (<t:1631999898:R>)**", value = f"""
```fix
{news}
```
        """)

        embed.set_footer(text=f"Suggested command: {prefix}{random.choice(list(self.context.bot.commands))} • Credits given in {prefix}credits")
        view = Stuff(ctx)


        view.message = await ctx.send(embed=embed, view=view) #without this line 233 would not work


    async def send_command_help(self, command):
        ctx = self.context
        alias = command.aliases
        description = command.help
        aliastext = "Aliases: ❌ This command has no aliases."
        descriptiontext = "Description: ❌ This command has no description."
        
        if alias:
            aliastext = f"Aliases: {', '.join(alias)}"
            
        if description:
            descriptiontext = f"Description: {command.help}"
            
        usable_by_you = 'No'
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                usable_by_you = 'Yes'
                
        owner_only = 'No'
        if 'is_owner' in command.checks:
            owner_only = 'Yes'
                
        embed = discord.Embed(title=f"Help - {command}", description=f"""
```diff
- <> = required argument
- [] = optional argument
```
```yaml
Usage: {self.get_minimal_command_signature(command)}
{aliastext}
{descriptiontext}
```
```yaml
Usable by you: {usable_by_you}
Owner only: {owner_only}
Slowmode: No
Permissions needed: No
```
                                  """)

        if command.brief:
            embed.set_image(url=command.brief)

        await ctx.send(embed=embed)


    async def send_cog_help(self, cog):
        ctx = self.context
        prefix = self.context.clean_prefix
        if cog.qualified_name.lower() == 'nsfw' and ctx.channel.is_nsfw() == False:
            raise commands.NSFWChannelRequired(ctx.channel)
        entries = cog.get_commands()
        command_signatures = [self.get_minimal_command_signature(c) for c in entries]
        if command_signatures:
            val = "\n".join(command_signatures)
            
            embed=discord.Embed(title=f"Help - {cog.qualified_name}", description=f"""
Total commands: {len(cog.get_commands())}
Commands usable by you (in this server): {len(await self.filter_commands(cog.get_commands(), sort=True))}
```diff
- <> = required argument
- [] = optional argument
+ Type {prefix}help [command] for help on a command
```
                                """)
            embed.add_field(name=f"Category: {cog.qualified_name}", value=f"""
{cog.description.split('|' )[0]} {cog.description.split('| ')[1]}
```yaml
{val}
```
                            """)

            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f"Help - {cog.qualified_name}", description=f"""
Total commands: {len(cog.get_commands())}
Commands usable by you (in this server): {len(await self.filter_commands(cog.get_commands(), sort=True))}
```diff
- <> = required argument
- [] = optional argument
+ Type {prefix}help [command] for help on a command
+ Description: {cog.description}
```
__**Available commands**__ **[{len(cog.get_commands())}]**
```yaml
This cog has no commands
```
                                """)
            await ctx.send(embed=embed)

    async def send_error_message(self, error):
        raise errors.CommandDoesntExist

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(description=f"{str(error.original)}")
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)

class ServerEmotesEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=10)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)

        embed = discord.Embed(title=f"{self.guild}'s emotes ({len(self.guild.emojis)})", description="\n".join(f'{i+1}. {v}' for i, v in enumerate(entries, start=offset)), timestamp=discord.utils.utcnow(), color=color)
        return embed
    
class ServerMembersEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=20)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        embed = discord.Embed(title=f"{self.guild}'s members ({self.guild.member_count})", description="\n".join(f'{i+1}. {v}' for i, v in enumerate(entries, start=offset)), timestamp=discord.utils.utcnow(), color=color)
        return embed
    
class ServerBotsEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=20)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        embed = discord.Embed(title=f"{self.guild}'s bots ()", description="\n".join(f'{i+1}. {v}' for i, v in enumerate(entries, start=offset)), timestamp=discord.utils.utcnow(), color=color)
        return embed

class ServerRolesEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=20)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        embed = discord.Embed(title=f"{self.guild}'s roles ({len(self.guild.roles)})", description="\n".join(f'{i+1}. {v}' for i, v in enumerate(entries, start=offset)), timestamp=discord.utils.utcnow(), color=color)
        return embed
    
class BotCommandsEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=20)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        embed = discord.Embed(title=f"{self.bot}'s commands ()", description="\n".join(f'{i+1}. {v}' for i, v in enumerate(entries, start=offset)), timestamp=discord.utils.utcnow(), color=color)
        return embed
    
class CharInfoEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=20)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        embed = discord.Embed(title=f"Character information", description="\n".join(entries), timestamp=discord.utils.utcnow(), color=color)
        return embed

def setup(client):
    client.add_cog(Info(client))

class Info(commands.Cog):
    "<:info:888768239889424444> | All informative commands like serverinfo, userinfo and more!"
    def __init__(self, client):
        self.client = client
        help_command = MyHelp()
        help_command.cog = self
        client.help_command = help_command
        
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
            'latest': 'https://enhanced-dpy.readthedocs.io/en/latest/',
            'latest-jp': 'https://discordpy.readthedocs.io/ja/latest',
            'python': 'https://docs.python.org/3',
            'python-jp': 'https://docs.python.org/ja/3',
            'master': 'https://enhanced-dpy.readthedocs.io/en/latest/',
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

        e = discord.Embed()
        cache = list(self._rtfm_cache[key].items())

        matches = finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

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

    @commands.command(
        help="Search lyrics of any song",
        aliases = ['l', 'lyrc', 'lyric'])
    async def lyrics(self, ctx, *, search):
        
        loadingEmbed = discord.Embed(title="Getting lyrics...")
        
        message = await ctx.send(embed=loadingEmbed)
        
        start = time.perf_counter()
        
        song = urllib.parse.quote(search)
        res = await self.client.session.get(f'https://evan.lol/lyrics/search/top?q={song}')
        if not 300 > res.status >= 200:
                return await ctx.send(f'Recieved poor status code of {res.status}')

        jsonData = await res.json()

        error = jsonData.get('error')
        if error:
            raise error

        lyrics = jsonData['lyrics']
        artist = jsonData['artists']['name']
        title = jsonData['name']
        thumbnail = jsonData['icon']['url']
        explicit = jsonData['explicit']
        length = jsonData['length']
        explicitStatus = "No"
        
        if explicit is True:
            explicitStatus = "Yes"

        end = time.perf_counter()
        
        ms = (end - start) * 1000
        
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        
        await message.delete()

        for chunk in textwrap.wrap(lyrics, 1536, replace_whitespace=False):
            embed = discord.Embed(title=f"{artist} - {title}", description=chunk, timestamp=discord.utils.utcnow(), color=color)
            embed.set_thumbnail(url=thumbnail)
            embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))} • Explicit? {explicitStatus} • Length: {length}", icon_url=ctx.author.avatar.url)
            
            await ctx.reply(embed=embed, footer=False)

    @commands.command(
        help="Shows you information about the member you mentioned",
        aliases=['ui', 'user', 'member', 'memberinfo'],
        brief="https://cdn.discordapp.com/attachments/876937268609290300/886407195279884318/userinfo.gif")
    @commands.cooldown(1, 5, BucketType.member)
    async def userinfo(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                
        fetchedMember = await self.client.fetch_user(member.id)
        guild = ctx.guild
        server = ctx.guild
        botStatus = "No"
        pendingStatus = "No"
        afkStatus = "No"
        blacklistedStatus = "No"
        premiumStatus = "Not boosting"
        acknowledgments = "None"
        statusEmote = "<:status_offline:596576752013279242>"
        nickname = member.nick
        desktopStatus = ":desktop: <:redTick:596576672149667840>"
        webStatus = ":globe_with_meridians: <:redTick:596576672149667840>"
        mobileStatus = ":mobile_phone:  <:redTick:596576672149667840>"

        if member.bot:
            botStatus = "Yes"

        if member.pending:
            pendingStatus = "Yes"
            
        if member.id in self.client.afk_users:
            afkStatus = "Yes"
            
        if member.id in self.client.blacklist:
            blacklistedStatus = "Yes"
            
        if member.premium_since:
            premiumStatus = f"{discord.utils.format_dt(member.premium_since, style='f')} ({discord.utils.format_dt(member.premium_since, style='R')})"

        if str(member.status).title() == "Online":
            statusEmote = "<:status_online:596576749790429200>"
            
        elif str(member.status).title() == "Idle":
            statusEmote = "<:status_idle:596576773488115722>"
            
        elif str(member.status).title() == "Dnd":
            statusEmote = "<:status_dnd:596576774364856321>"
            
        elif str(member.status).title() == "Streaming":
            statusEmote = "<:status_streaming:596576747294818305>"
        
        if member.id == 564890536947875868:
            acknowledgments = ":crown: Owner"
            
        elif member.id == 349373972103561218:
            acknowledgments = "Helped with a lot of stuff"
            
        if member.nick is None:
            nickname = f"{member.name} (No nickname)"

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

        if member.avatar:
            if member.avatar.is_animated() == True:
                avatar = f"[PNG]({member.avatar.replace(format='png', size=2048).url}) **|** [JPG]({member.avatar.replace(format='jpg', size=2048).url}) **|** [JPEG]({member.avatar.replace(format='jpeg', size=2048).url}) **|** [WEBP]({member.avatar.replace(format='webp', size=2048).url}) **|** [GIF]({member.avatar.replace(format='gif', size=2048).url})"
            else:
                avatar = f"[PNG]({member.avatar.replace(format='png', size=2048).url}) **|** [JPG]({member.avatar.replace(format='jpg', size=2048).url}) **|** [JPEG]({member.avatar.replace(format='jpeg', size=2048).url}) **|** [WEBP]({member.avatar.replace(format='webp', size=2048).url})"
        else:
            avatar = f"User has no avatar."

        fetchedMember = await self.client.fetch_user(member.id)

        if fetchedMember.banner:
            if fetchedMember.banner.is_animated() == True:
                banner = f"[PNG]({fetchedMember.banner.replace(format='png', size=2048).url}) **|** [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) **|** [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) **|** [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url}) **|** [GIF]({fetchedMember.banner.replace(format='gif', size=2048).url})"
            else:
                banner = f"[PNG]({fetchedMember.avatar.replace(format='png', size=2048).url}) **|** [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) **|** [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) **|** [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url})"
        else:
            banner = "No banner found"

        if str(member.desktop_status) == "online" or str(member.desktop_status) == "idle" or str(member.desktop_status) == "dnd" or str(member.desktop_status) == "streaming":
            desktopStatus = ":desktop: <:greenTick:596576670815879169>"

        if str(member.web_status) == "online" or str(member.web_status) == "idle" or str(member.web_status) == "dnd" or str(member.web_status) == "streaming":
            webStatus = ":globe_with_meridians: <:greenTick:596576670815879169>"

        if str(member.mobile_status) == "online" or str(member.mobile_status) == "idle" or str(member.mobile_status) == "dnd" or str(member.mobile_status) == "streaming":
            mobileStatus = ":mobile_phone: <:greenTick:596576670815879169>"

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


        embed = discord.Embed(title=f"{member}", url=f"https://discord.com/users/{member.id}", description=f"""
<:nickname:876507754917929020> Nickname: {nickname}
:hash: Discriminator:  #{member.discriminator}
Mention: {member.mention}
<:greyTick:596576672900186113> ID: {member.id}

:robot: Bot?: {botStatus}
Pending verification?: {pendingStatus}
AFK?: {afkStatus}
Blacklisted?: {blacklistedStatus}

Avatar url: {avatar}
Banner url: {banner}

<:boost:858326699234164756> Boosting: {premiumStatus}
<:invite:895688440639799347> Created: {discord.utils.format_dt(member.created_at, style="f")} ({discord.utils.format_dt(member.created_at, style="R")})
<:joined:895688440786595880> Joined: {discord.utils.format_dt(member.joined_at, style="f")} ({discord.utils.format_dt(member.joined_at, style="R")})
<:moved:895688440543342625> Join position:
```yaml
{join_seq}
```

Mutual guilds: {len(member.mutual_guilds)}

{statusEmote} Current status: {str(member.status).title()}
:video_game: Current activity: {str(member.activity.type).split('.')[-1].title() if member.activity else 'Not playing'} {member.activity.name if member.activity else ''}
<:discord:877926570512236564> Client: {desktopStatus} **|** {webStatus} **|** {mobileStatus}

<:role:895688440513974365> Top Role: {member.top_role.mention}
<:role:895688440513974365> Roles: {roles}
<:store_tag:896379579973894155> Staff permissions: {perms}
<:store_tag:896379579973894155> Badges: {badges}
Acknowledgments: {acknowledgments}

:rainbow: Color: {member.color}
:rainbow: Accent color: {fetchedMember.accent_color}
        """)
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        await ctx.send(embed=embed)


    @commands.command(
        help="Shows you information about the server",
        aliases=['si', 'guild', 'guildinfo'])
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
        
    @commands.command(
        help="Shows information about a emoji",
        aliases=['ei', 'emoteinfo', 'emoinfo', 'eminfo', 'emojinfo', 'einfo'])
    async def emojiinfo(self, ctx, emoji : typing.Union[discord.Emoji, discord.PartialEmoji]):
        if isinstance(emoji, discord.Emoji):
            fetchedEmoji = await ctx.guild.fetch_emoji(emoji.id)
            url = f"{emoji.url}"
            available = "No"
            managed = "No"
            animated = "No"
            user = f"{fetchedEmoji.user}"
            
            view = discord.ui.View()
            style = discord.ButtonStyle.gray
            item = discord.ui.Button(style=style, emoji="🔗", label="Emoji link", url=url)
            view.add_item(item=item)
            
            if fetchedEmoji.user is None:
                user = "Couldn't get user"
            
            if emoji.available:
                available = "Yes"
                
            if emoji.managed:
                managed = "Yes"
            
            if emoji.animated:
                animated = "Yes"

            embed = discord.Embed(title=f"{emoji.name}", description=f"""
Name: {emoji.name}
<:greyTick:860644729933791283> ID: {emoji.id}

Created at: {discord.utils.format_dt(emoji.created_at, style="f")} ({discord.utils.format_dt(emoji.created_at, style="R")})
:link: Link: [Click here]({url})

<:servers:870152102759006208> Created by: {user}
Guild: {emoji.guild} ({emoji.id})

Available?: {available}
<:twitch:889903398672035910> Managed?: {managed}
<:emoji_ghost:658538492321595393> Animated?: {animated}
                                """)
            embed.set_image(url=emoji.url)
            
            await ctx.send(embed=embed, view=view)
        elif isinstance(emoji, discord.PartialEmoji):
            url = f"{emoji.url}"
            animated = "No"
            
            view = discord.ui.View()
            style = discord.ButtonStyle.gray
            item = discord.ui.Button(style=style, emoji="🔗", label="Emoji link", url=url)
            view.add_item(item=item)
            
            if emoji.animated:
                animated = "Yes"

            embed = discord.Embed(title=f"{emoji.name}", description=f"""
Name: {emoji.name}
<:greyTick:860644729933791283> ID: {emoji.id}

Created at: {discord.utils.format_dt(emoji.created_at, style="f")} ({discord.utils.format_dt(emoji.created_at, style="R")})
:link: Link: [Click here]({url})

<:emoji_ghost:658538492321595393> Animated?: {animated}
                                """)
            embed.set_image(url=emoji.url)
            
            await ctx.send(embed=embed, view=view)
        else:
            raise errors.UnknownError
        
    @commands.command(
        help="Shows information about the bot",
        aliases=['bi'])
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
                    
        ver = sys.version_info
        full_version = f"{ver.major}.{ver.minor}.{ver.micro}"

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
Commands used: {self.client.commands_used}

:file_folder: Files: {fc}
Lines: {ls:,}
Classes: {cl}
Functions: {fn}
Coroutine: {cr}
:hash: Comments: {cm:,}

Enhanced-dpy version: {discord.__version__}
Python version: {full_version}

        """)
        embed.set_thumbnail(url=self.client.user.avatar.url)

        await ctx.send(embed=embed)
        
    async def send_permissions(self, ctx, member):
        permissions = [permission for permission in member.guild_permissions]
        
        allowed = []
        denied = []
        
        allowed_emote = "<a:y_:891733484459163729>"
        denied_emote = "<a:n_:891733484933120021>"
        
        for name, value in permissions:
            name = name.replace("_", " ").replace("guild", "server").title()
            
            if value:
                allowed.append(f"{allowed_emote} {name}")
                               
            else:
                denied.append(f"{denied_emote} {name}")

        if f"{allowed_emote} Administrator" in allowed:
            allowed = [f"{allowed_emote} Administrator"]
            
        if len(denied) == 0:
            denied = [f"{denied_emote} None"]
        
        allowed = '\n'.join(allowed)
        denied = '\n'.join(denied)
        
        embed = discord.Embed(title=f"{member}'s permissions")
        embed.add_field(name="Allowed", value=f"{allowed}", inline=True)
        embed.add_field(name="Denied", value=f"{denied}", inline=True)
        
        await ctx.send(embed=embed)
            
    @commands.command(
        help="Shows you what permissions the bot has in the current server",
        aliases=['perms', 'permission'])
    async def permissions(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
            
        await self.send_permissions(ctx, member)

    @commands.command(
        help="Shows a list of commands this bot has",
        aliases=['commands', 'command', 'cmds', 'commandslist', 'cmdslist', 'commands_list', 'cmds_list', 'commandlist', 'cmdlist', 'command_list', 'cmd_list'])
    async def _commands(self, ctx):
        bot = ctx.me.display_name
        botCommands = self.client.commands
        commands = []
    

        for command in botCommands:

            commands.append(f"{command.name}")

        paginator = ViewMenuPages(source=ServerBotsEmbedPage(commands, bot), clear_reactions_after=True)
        page = await paginator._source.get_page(0)
        kwargs = await paginator._get_kwargs_from_page(page)
        if paginator.build_view():
            paginator.message = await ctx.send(embed=kwargs['embed'],view = paginator.build_view())
        else:
            paginator.message = await ctx.send(embed=kwargs['embed'])
        await paginator.start(ctx)

    @commands.command(
        help="Shows you a list of emotes from this server",
        aliases=['emojilist', 'emote_list', 'emoji_list', 'emotes', 'emojis'])
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
        
    @commands.command(
    help="Shows you a list of members from this server",
    aliases=['member_list', 'memlist', 'mem_list', 'members'])
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
        
    @commands.command(
        help="Shows you a list of bots from this server",
        aliases=['bot_list', 'bolist', 'bo_list', 'bots', 'bot'])
    async def botlist(self, ctx, id : int=None):
        if id:
            guild = self.client.get_guild(id)
            if not guild:
                return await ctx.send("I couldn't find that server. Make sure the ID you entered was correct.")
        else:
            guild = ctx.guild

        guildBots = list(filter(lambda m : m.bot, guild.members))
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
        
    @commands.command(
        help="Shows you a list of roles from this server",
        aliases=['role_list', 'rolist', 'ro_list', 'roles', 'role'])
    async def rolelist(self, ctx, id : int=None):
        if id:
            guild = self.client.get_guild(id)
            if not guild:
                return await ctx.send("I couldn't find that server. Make sure the ID you entered was correct.")
        else:
            guild = ctx.guild

        guildRoles = guild.roles
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

    @commands.command(
        help="Shows information about the channel",
        aliases=['ci', 'channel'])
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
        
    @commands.command(
        help="Shows information about a message",
        aliases=['mi'])
    async def messageinfo(self, ctx, message : discord.Message=None):
        if message is None:
            if ctx.message.reference:
                message = ctx.message.reference.resolved
            else:
                message = ctx.message
                
        message = ctx.channel.get_partial_message(message.id)
        embed = discord.Embed(title="Message information", description=f"""
ID: {message.id}

Server: {message.guild} ({message.guild.id})
Channel: {message.channel.mention} ({message.channel.id})

Sent at: 

Jump URL: [Click here]({message.jump_url})
        """)

        await ctx.send(embed=embed)

    @commands.command(
        help="Shows the avatar of the member you mentioned",
        aliases=['av'])
    @commands.cooldown(1, 5, BucketType.member)
    async def avatar(self, ctx, member : discord.Member=None):
        errorMessage = f"{member} doesnt have a avatar."
        member = member or ctx.author
            
            
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
            
    @commands.group(
        invoke_without_command=True,
        aliases=['bn'])
    async def banner(self, ctx):
        fetchedMember = await self.client.fetch_user(ctx.author.id)
        url = fetchedMember.banner
        
        if url == None:
            return await ctx.send("You don't have a banner!")
        
        if fetchedMember.banner.is_animated() == True:
            text = f"[PNG]({fetchedMember.banner.replace(format='png', size=2048).url}) | [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) | [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) | [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url}) | [GIF]({fetchedMember.banner.replace(format='gif', size=2048).url})"
            
        else:
            text = f"[PNG]({fetchedMember.banner.replace(format='png', size=2048).url}) | [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) | [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) | [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url})"
        
        embed = discord.Embed(title=f"{ctx.author.name}'s banner", description=text)
        embed.set_image(url=url)
        
        await ctx.send(embed=embed)

    @banner.command(aliases=['guild'])
    async def server(self, ctx):
        server = ctx.guild
        url = server.banner
        
        if url == None:
            return await ctx.send("This server doesn't have a banner!")
        
        if server.banner.is_animated() == True:
            text = f"[PNG]({server.banner.replace(format='png', size=2048).url}) | [JPG]({server.banner.replace(format='jpg', size=2048).url}) | [JPEG]({server.banner.replace(format='jpeg', size=2048).url}) | [WEBP]({server.banner.replace(format='webp', size=2048).url}) | [GIF]({server.banner.replace(format='gif', size=2048).url})"
            
        else:
            text = f"[PNG]({server.banner.replace(format='png', size=2048).url}) | [JPG]({server.banner.replace(format='jpg', size=2048).url}) | [JPEG]({server.banner.replace(format='jpeg', size=2048).url}) | [WEBP]({server.banner.replace(format='webp', size=2048).url})"
        
        embed = discord.Embed(title=f"{server.name}'s banner", description=text)
        embed.set_image(url=url)
        
        await ctx.send(embed=embed)
        
    @banner.command(aliases=['user'])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def member(self, ctx, member : discord.Member=None):
        errorMessage = f"{member} doesn't have a banner!"
        
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                errorMessage = "You don't have a banner!"
                
        fetchedMember = await self.client.fetch_user(member.id)
        url = fetchedMember.banner
        
        if url is None:
            return await ctx.send(errorMessage)
        
        if fetchedMember.banner.is_animated() == True:
            text = f"[PNG]({fetchedMember.banner.replace(format='png', size=2048).url}) | [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) | [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) | [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url}) | [GIF]({fetchedMember.banner.replace(format='gif', size=2048).url})"
            
        else:
            text = f"[PNG]({fetchedMember.banner.replace(format='png', size=2048).url}) | [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) | [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) | [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url})"
        
        embed = discord.Embed(title=f"{member}'s banner", description=text)
        embed.set_image(url=url)
        
        await ctx.send(embed=embed)
        
    # @commands.command(help="Shows the banner of the member you mentioned", aliases=['bn'])
    # @commands.cooldown(1, 5, BucketType.member)
    # async def banner(self, ctx, member : discord.Member=None):
    #     if member is None:
    #         if ctx.message.reference:
    #             member = ctx.message.reference.resolved.author
    #             errorMessage = f"{member} doesn't have a banner"
    #         else:
    #             member = ctx.author
    #             errorMessage = "You don't have a banner"

    #     fetchedMember = await self.client.fetch_user(member.id)

    #     if fetchedMember.banner:
            
    #         if fetchedMember.banner.is_animated() == True:
    #             text = f"[PNG]({fetchedMember.banner.replace(format='png', size=2048).url}) | [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) | [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) | [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url}) | [GIF]({fetchedMember.banner.replace(format='gif', size=2048).url})"
                
    #         else:
    #             text = f"[PNG]({fetchedMember.banner.replace(format='png', size=2048).url}) | [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) | [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) | [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url})"
                
    #         embed=discord.Embed(title=f"{member}'s avatar", description=f"{text}")
    #         embed.set_image(url=fetchedMember.banner.url)

    #         await ctx.send(embed=embed)
    #     else:
    #         await ctx.send(f"{errorMessage}")

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

        # discords = time.monotonic()
        # url = "https://discordapp.com/"
        # resp = await self.client.session.get(url)
        # if resp.status == 200:
        #         discorde = time.monotonic()
        #         discordms = (discorde - discords) * 1000
        #         pings.append(discordms)
        # else:
        #         discordms = 0

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
        # discord_latency = f"{round(discordms)}ms{' ' * (9-len(str(round(discordms, 3))))}"
        database_latency = f"{round(psqlms)}ms{' ' * (9-len(str(round(psqlms, 3))))}"
        average_latency = f"{round(average)}ms{' ' * (9-len(str(round(average, 3))))}"

        embed = discord.Embed(title="Pong!")
        embed.add_field(name=":globe_with_meridians: Websocket latency", value=f"{websocket_latency}")
        embed.add_field(name="<a:typing:597589448607399949> Typing latency", value=f"{typing_latency}")
        embed.add_field(name=":speech_balloon: Message latency", value=f"{message_latency}")
        # embed.add_field(name="<:discord:877926570512236564> Discord latency", value=f"{discord_latency}")
        embed.add_field(name="<:psql:896134588961800294> Database latency", value=f"{database_latency}")
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
        
    @commands.command(help="Shows you how the bot is feeling", aliases=['feeling', 'howthebotdoin', 'how_the_bot_doin', 'is_it_okay', 'is_the_bot_ok'])
    async def isitok(self, ctx):
        with open('./data/botStatus.txt') as f:
            botStatusFileContent = f.read()
            status = botStatusFileContent
            
        embed = discord.Embed(description=status)
        
        await ctx.send(embed=embed)

    @commands.command(help="Shows how many servers the bot is in", aliases=['guilds'])
    async def servers(self, ctx):
        embed = discord.Embed(title=f"I'm in `{len(self.client.guilds)}` servers.")

        await ctx.send(embed=embed)

    @commands.command(help="Shows how many messages the bot has seen", aliases=['msg', 'msgs', 'message'])
    async def messages(self, ctx):
        embed = discord.Embed(title=f"I've a total of `{self.client.messages}` messages and `{self.client.edited_messages}` edits.")
        
        await ctx.send(embed=embed)

    @commands.command()
    async def snipe(self, ctx):
        embed = discord.Embed(description=f"{self.client.last_message}")
        embed.set_author(name=f"{self.client.last_message_author} ({self.client.last_message_author.id}) said in #{self.client.last_message_channel}:", url=f"{self.client.last_message_author.avatar.url}")
        embed.add_field(name="Deletion date:", value=f"Message was deleted at {discord.utils.format_dt(self.client.last_message_deletion_date, style='R')}")

        await ctx.send(embed=embed)

    @commands.command(help="Sends a suggestion", aliases=['bot_suggestion', 'suggestion', 'make_suggestion', 'botsuggestion', 'makesuggestion'])
    async def suggest(self, ctx, *, suggestion):
        if len(suggestion) > 750:
            return await ctx.send("Your suggestion exceeded the 750-character limit.")
        
        confirmation = await ctx.confirm(message="Are you sure you want to send this suggestion?",
                                        delete_after_confirm=True,
                                        delete_after_cancel=True,
                                        delete_after_timeout=True,
                                        buttons=(('✔️', f'Yes', discord.ButtonStyle.green), ('✖️', f'No', discord.ButtonStyle.red)), timeout=15)

        if confirmation == True:
            await ctx.send("Okay, I've sent your suggestion to the owner.")
            
            channel = self.client.get_channel(879786064473129033)
            
            author = ctx.author
            message = ctx.message
            
            colors = [0x910023, 0xA523FF]
            color = random.choice(colors)
            
            embed = discord.Embed(title="New suggestion!", description=f"""
__**Author info**__

Name: `{author}`
ID: `{author.id}`
Mention: `{author.mention}`
Tag: `#{author.discriminator}`

__**Suggestion info**__

Suggestion: `{suggestion}`
Length: `{len(suggestion)}`
URL: [Click here]({message.jump_url}/ 'Jump URL')
                                """, timestamp=discord.utils.utcnow(), color=color)
            
            return await channel.send(embed=embed)

        else:
            return await ctx.send("Okay, I've cancelled your suggestion.")

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
Did some PRs on my github: Someone#5555
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
    async def afk(self, ctx, *, reason="No reason provided"):
        if ctx.author.id in self.client.afk_users and ctx.author.id in self.client.auto_un_afk and self.client.auto_un_afk[ctx.author.id] is True:
            return
        
        if ctx.author.id not in self.client.afk_users:
            await self.client.db.execute("INSERT INTO afk (user_id, start_time, reason) VALUES ($1, $2, $3) "
                                      "ON CONFLICT (user_id) DO UPDATE SET start_time = $2, reason = $3",
                                      ctx.author.id, ctx.message.created_at, reason[0:1800])
            self.client.afk_users[ctx.author.id] = True
            
            embed = discord.Embed(title=f"<:idle:872784075591675904> {ctx.author.name} is now AFK", description=f"Reason: {reason}")
            
            await ctx.send(embed=embed)
            
        else:
            self.client.afk_users.pop(ctx.author.id)

            info = await self.client.db.fetchrow("SELECT * FROM afk WHERE user_id = $1", ctx.author.id)
            await self.client.db.execute("INSERT INTO afk (user_id, start_time, reason) VALUES ($1, null, null) "
                                      "ON CONFLICT (user_id) DO UPDATE SET start_time = null, reason = null", ctx.author.id)
            
            delta_uptime = discord.utils.utcnow() - info["start_time"]
            hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            
            embed = discord.Embed(title=f"👋 Welcome back {ctx.author.name}!", description=f"You've been afk for {days} days, {hours} hours, {minutes} minutes and {seconds} seconds.\nReason: {info['reason']}")
            
            await ctx.send(embed=embed)

            await ctx.message.add_reaction("👋")

    @commands.command(help="Toggles if the bot should remove your AFK status after you send a message or not", aliases=['auto_un_afk', 'aafk', 'auto-afk-remove'])
    async def autoafk(self, ctx, mode : bool = None):
        mode = mode or (False if (ctx.author.id in self.client.auto_un_afk and self.client.auto_un_afk[ctx.author.id] is True) or ctx.author.id not in self.client.auto_un_afk else True)
        self.client.auto_un_afk[ctx.author.id] = mode
        
        await self.client.db.execute("INSERT INTO afk (user_id, auto_un_afk) VALUES ($1, $2) "
                                  "ON CONFLICT (user_id) DO UPDATE SET auto_un_afk = $2", ctx.author.id, mode)
        
        text = f'{"Enabled" if mode is True else "Disabled"}'
                                  
        embed = discord.Embed(title=f"{ctx.toggle(mode)} {text} automatic AFK removal", description="To remove your AFK status do `afk` again.")
                                  
        return await ctx.send(embed=embed)

    # @commands.command()
    # async def afk(self, ctx, *, reason="No reason provided"):
    #     if len(reason) > 100:
    #         return await ctx.send("Reason cannot be over 100 characters.")
        
    #     try:
    #         await member.edit(nick=f"[AFK] {ctx.author.display_name}")
    #     except:
    #         pass

    #     await self.client.db.execute('INSERT INTO afk (user_id, start_time, reason) VALUES ($1, $2, $3) '
    #                               'ON CONFLICT (user_id) DO UPDATE SET start_time = $2, reason = $3',
    #                               ctx.author.id, ctx.message.created_at, reason[0:1800])
        
    #     self.client.afk_users[ctx.author.id] = True
        
    #     embed = discord.Embed(title=f"<:status_idle:596576773488115722> {ctx.author.name} is now afk cause: {reason}")

    #     await ctx.send(embed=embed)

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

    @commands.group(help="Gives you a documentation link for a enhanced-discord.py entity", aliases=['rtfd'], invoke_without_command=True)
    async def rtfm(self, ctx, *, entity : str=None):
        key = self.transform_rtfm_language_key(ctx, 'latest')
        await self.do_rtfm(ctx, key, entity)
        
    @commands.group(help="Gives you a documentation link for a enhanced-discord.py entity", aliases=['edpy', 'dpy'], invoke_without_command=True)
    async def rtfm_edpy(self, ctx, *, entity : str=None):
        key = self.transform_rtfm_language_key(ctx, 'latest')
        await self.do_rtfm(ctx, key, entity)

    @rtfm.command(help="Gives you a documentation link for a Python entity", name="python", aliases=['py'])
    async def rtfm_python(self, ctx, *, entity : str=None):
        key = self.transform_rtfm_language_key(ctx, 'python')
        await self.do_rtfm(ctx, key, entity)