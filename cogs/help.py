from discord.ext import commands
import discord
import datetime
import helpers
import contextlib
import random
import asyncio
import errors
import os
from typing import Any, Dict, List, Optional, Union

# copied code from stella

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
    def __init__(self, ctx):
        self.ctx = ctx
        options = [
            
            discord.SelectOption(label='Info', description='Info', emoji=':info:'),
            discord.SelectOption(label='Fun', description='Fun', emoji='⚽'),
            discord.SelectOption(label='Misc', description='Misc', emoji='⚙️'),
            discord.SelectOption(label='Mod', description='Mod', emoji=':staff:'),
            discord.SelectOption(label='Music', description='Music', emoji=':music:'),
            discord.SelectOption(label='Owner', description='Owner', emoji=':owner_crown:'),
            discord.SelectOption(label='Custom', description='Custom', emoji='🎉'),
            discord.SelectOption(label='Images', description='Images', emoji='🖼️'),
            
        ]

        super().__init__(placeholder='Select a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        cog = self.ctx.bot.get_cog(self.values[0])
        embed = discord.Embed(title=f"Help - {self.values[0]}", description=f"""
Total commands: {len(cog.get_commands())}
Commands usable by you (in this server): {len(await self.filter_commands(cog.get_commands(), sort=True))}
```diff
- <> = required argument
- [] = optional argument
+ Type help [command] for help on a command
```
`Description:` {cog.description.split('|')[0]}
`{cog.description.split('|')[1]}`

__**Available commands**__ **[{len(cog.get_commands())}]**
```fix

```
                              """)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class VoteButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(emoji="<:topgg:870133913102721045>", label='top.gg', url="https://top.gg/bot/760179628122964008"))
        self.add_item(discord.ui.Button(emoji="<:botsgg:870134146972938310>", label='bots.gg', url="https://discord.bots.gg/bots/760179628122964008"))

class Stuff(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.add_item(Dropdown(self.ctx))
        url = "https://discord.com/api/oauth2/authorize?client_id=760179628122964008&permissions=8&scope=bot"
        self.add_item(discord.ui.Button(emoji="<:invite:860644752281436171>", label='Invite me', url=url))
        self.add_item(discord.ui.Button(emoji="<:github:744345792172654643>", label='Source code', url="https://github.com/Ender2K89/Stealth-Bot"))

    @discord.ui.button(label='Vote', style=discord.ButtonStyle.gray, emoji="<:topgg:870133913102721045>")
    async def receive(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed=discord.Embed(title="Vote for me")
        await interaction.response.send_message(embed=embed, ephemeral=True, view=VoteButtons())

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
        with open('./data/news.txt') as f:
            newsFileContext = f.read()
            new1 = f"{newsFileContext}"
            news = new1.replace("%%PREFIX%%", f"{prefix}")
        embed = discord.Embed(title="Help", description=f"""
Prefix: `{prefix}`
Total commands: `{len(list(self.context.bot.commands))}`
Commands usable by you (in this server): `{len(await self.filter_commands(list(self.context.bot.commands), sort=True))}`
Written with `{count_python('.'):,}` lines.
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
        embed.add_field(name=f"<:category:882685952999428107> __**Available categories**__ **[{len(allcogs)}]**", value=f"""
{nl.join(allcogs)}
        """)

        embed.add_field(name="📰 __**Latest News**__ - **<t:1631999898:d> (<t:1631999898:R>)**", value = f"""
```fix
{news}
```
        """)

        embed.set_footer(text=f"Suggested command: {prefix}{random.choice(list(self.context.bot.commands))} • Credits given in {prefix}credits")

        await ctx.send(embed=embed, view=Stuff(ctx))


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
        if cog.qualified_name.lower() == 'nsfw':
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
`Description:` {cog.description.split('|')[0]}
`{cog.description.split('|')[1]}`

__**Available commands**__ **[{len(cog.get_commands())}]**
```fix
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
```fix
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


class Help(commands.Cog):
    ":question: | The help command, how did you find this though..."
    def __init__(self, client):
        self.client = client
        self.hidden = True
        help_command = MyHelp()
        help_command.cog = self
        client.help_command = help_command

def setup(client):
    client.add_cog(Help(client))
