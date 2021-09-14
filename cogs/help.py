from discord.ext import commands
import discord
import datetime
import helpers
import random
import os

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
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Red', description='Your favourite colour is red', emoji='🟥'),
            discord.SelectOption(label='Green', description='Your favourite colour is green', emoji='🟩'),
            discord.SelectOption(label='Blue', description='Your favourite colour is blue', emoji='🟦')
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}', ephemeral=True)

class VoteButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(emoji="<:topgg:870133913102721045>", label='top.gg', url="https://top.gg/bot/760179628122964008"))
        self.add_item(discord.ui.Button(emoji="<:botsgg:870134146972938310>", label='bots.gg', url="https://discord.bots.gg/bots/760179628122964008"))

class Stuff(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(emoji="<:invite:860644752281436171>", label='Invite me', url="https://discord.com/api/oauth2/authorize?client_id=760179628122964008&permissions=8&scope=bot"))
        self.add_item(discord.ui.Button(emoji="<:github:744345792172654643>", label='Source code', url="https://github.com/Ender2K89/Stealth-Bot"))
        self.add_item(Dropdown())

    @discord.ui.button(label='Vote', style=discord.ButtonStyle.gray, emoji="<:topgg:870133913102721045>")
    async def receive(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed=discord.Embed(title="Vote for me", color=0x2F3136)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=VoteButtons())

class MyHelp(commands.HelpCommand):
    def get_minimal_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)



    def get_command_name(self, command):
        return '%s' % (command.qualified_name)



    async def send_bot_help(self, mapping):
        ctx = self.context
        prefix = await self.context.bot.db.fetchval('SELECT prefix FROM guilds WHERE guild_id = $1', ctx.guild.id)
        prefix = prefix or 'sb!'
        with open('./data/news.txt') as f:
            newsFileContext = f.read()
            new1 = f"{newsFileContext}"
            news = new1.replace("%%PREFIX%%", f"{prefix}")
        embed = discord.Embed(title="Help", description=f"""
Total commands: `{len(list(self.context.bot.commands))}`
Commands usable by you (in this server): `{len(await self.filter_commands(list(self.context.bot.commands), sort=True))}`
Written with `{count_python('.'):,}` lines.
```diff
+ Type {prefix}help [command/category] for help on a command/category
- <> = required argument
- [] = optional argument
```
                              """, timestamp=discord.utils.utcnow(), color=0x2F3136)

        allcogs = []
        cogindex = []
        ignored_cogs=['help', 'Jishaku', 'events']
        iter = 1
        for cog, commands in mapping.items():
            if cog is None or cog.qualified_name in ignored_cogs: continue
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_name(c) for c in filtered]
            if command_signatures:
                num = f"{iter}\U0000fe0f\U000020e3"
                cogindex.append(cog.qualified_name)
                allcogs.append(f"{num} {cog.qualified_name}")
                iter+=1
        nl = '\n'
        embed.add_field(name=f"<:category:882685952999428107> __**Available categories**__ **[{len(allcogs)}]**", value=f"""
```fix
{nl.join(allcogs)}
```
        """)

        embed.add_field(name="📰 __**Latest News**__ - **<t:1631558059:d> (<t:1631558059:R>)**", value = f"""
```fix
{news}
```
                        """)

        embed.set_footer(text=f"Suggested command: {prefix}{random.choice(list(self.context.bot.commands))} • Credits given in {prefix}credits")

        await ctx.reply(embed=embed, view=Stuff())



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
                                  """, timestamp=discord.utils.utcnow(), color=0x2F3136)

        if command.brief:
            embed.set_image(url=command.brief)

        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.reply(embed=embed)



    async def send_cog_help(self, cog):
        ctx = self.context
        prefix = await self.context.bot.db.fetchval('SELECT prefix FROM guilds WHERE guild_id = $1', ctx.guild.id)
        prefix = prefix or 'sb!'
        entries = cog.get_commands()
        command_signatures = [self.get_minimal_command_signature(c) for c in entries]
        if command_signatures:
            val1 = "\n".join(command_signatures)
            val = val1.replace('10️⃣', '1️⃣0️⃣')
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
{val}
```
                                """, timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed)
        else:
            embed=discord.Embed(title=f"Help - {cog.qualified_name}", description=f"""
This cog has no commands.
                                """, timestamp=discord.utils.utcnow(), color=0x2F3136)
            await ctx.reply(embed=embed)


class help(commands.Cog):
    def __init__(self, client):
        self.client = client
        help_command = MyHelp()
        help_command.cog = self
        client.help_command = help_command

def setup(client):
    client.add_cog(help(client))
