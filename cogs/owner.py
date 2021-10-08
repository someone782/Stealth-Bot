import discord
import helpers.helpers as helpers
import datetime
import asyncio
import os
import typing
import time
import textwrap
import asyncpg
import traceback
import sys
import shutil
import pathlib
import errors
import jishaku
import psutil
import lavalink
import random
import itertools
from discord.ext import commands, menus
from discord.ext.menus.views import ViewMenuPages
import importlib
import jishaku.modules
import io
import contextlib
from jishaku.codeblocks import Codeblock, codeblock_converter
from jishaku.features.baseclass import Feature
from jishaku.models import copy_context_with
from jishaku.paginators import WrappedPaginator

def setup(client):
    client.add_cog(Owner(client))
    
def cleanup_code(content):
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    # remove `foo`
    return content.strip('` \n')

def get_cpu_usage_pct():
    return psutil.cpu_percent(interval=0.5)

def get_ram_usage():
    return int(psutil.virtual_memory().total - psutil.virtual_memory().available)

def get_ram_total():
    return int(psutil.virtual_memory().total)

def get_ram_usage_pct():
    return psutil.virtual_memory().percent

class BlacklitedUsersEmbedPage(menus.ListPageSource):
    def __init__(self, data):
        self.data = data
        super().__init__(data, per_page=20)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        embed = discord.Embed(title=f"Blacklisted users", description="\n".join(entries), timestamp=discord.utils.utcnow(), color=color)
        return embed

class Owner(commands.Cog):
    "<:owner_crown:845946530452209734> | Commands that only the developer of this bot can use"
    def __init__(self, client):
        self.hidden = True
        self.client = client
        self._last_result = None
        
    @commands.command(help="Shows information about the system the bot is hosted on",
                      aliases=['sys'])
    async def system(self, ctx):
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        
        start = time.perf_counter()
        
        pid = os.getpid()
        process = psutil.Process(pid)
        total, used, free = shutil.disk_usage("/")
        ver = sys.version_info
        full_version = f"{ver.major}.{ver.minor}.{ver.micro}"
        
        delta_uptime = discord.utils.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
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
                    
        pings = []
        number = 0

        typings = time.monotonic()
        await ctx.trigger_typing()
        typinge = time.monotonic()
        typingms = (typinge - typings) * 1000
        pings.append(typingms)

        start2 = time.perf_counter()
        message = await ctx.send("Getting system information...")
        end2 = time.perf_counter()
        messagems = (end2 - start2) * 1000
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
                    
        end = time.perf_counter()

        ms = (end - start) * 1000

        embed = discord.Embed(description=f"""
```yaml
PID: {os.getpid()}
CPU: {psutil.cpu_percent()}% / 100% ({get_cpu_usage_pct()}%)
RAM: {int(get_ram_usage() / 1024 / 1024)}MB / {int(get_ram_total() / 1024 / 1024)}MB ({get_ram_usage_pct()}%)
Disk: {used // (2**30)}GB / {total // (2**30)}GB
Uptime: {days} days, {hours} hours, {minutes} minutes and {seconds} seconds
```
                              """, timestamp=discord.utils.utcnow(), color=color)
        
        embed.add_field(name="\u200b", value=f"""
```yaml
Files: {fc}
Lines: {ls:,}
Classes: {cl}
Functions: {fn}
Coroutine: {cr}
Comments: {cm:,}
```
                        """, inline=True)
        
        embed.add_field(name="\u200b", value=f"""
```yaml
PostgreSQL:
Lavalink: {lavalink.__version__}
e-dpy: {discord.__version__}
asyncpg: {asyncpg.__version__}
Python: {full_version}
Idk: 69.42
```
                        """, inline=True)
        
        embed.add_field(name="\u200b", value=f"""
```yaml
Websocket: {websocket_latency}
Typing: {typing_latency}
Message: {message_latency}
Database: {database_latency}
Average: {average_latency}
```
                        """, inline=True)
        
        embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))}", icon_url=ctx.me.avatar.url)
        
        await message.edit(content="Received system information!", embed=embed)

    @commands.command(help="Evaluates code")
    @commands.is_owner()
    async def eval(self, ctx, *, body : str):
        env = {
            'bot': self.client,
            'client': self.client,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'server': ctx.guild,
            '_': self._last_result
        }

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            try:
                await ctx.message.add_reaction('<:redTick:596576672149667840>')
            except (discord.Forbidden, discord.HTTPException):
                pass
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('<:redTick:596576672149667840>')
            except (discord.Forbidden, discord.HTTPException):
                pass
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('<:greenTick:596576670815879169>')
            except (discord.Forbidden, discord.HTTPException):
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

        
    @commands.command(
        help="Unloads an cog",
        aliases=['unl', 'ue', 'uc'])
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    @commands.is_owner()
    async def unload(self, ctx, extension):
        embed = discord.Embed(description=f":arrow_down: {extension}")
        message = await ctx.send(embed=embed)
        
        try:
            self.client.unload_extension(f"cogs.{extension}")
            embed = discord.Embed(description=f"<:redTick:596576672149667840> {extension}")
            
            await message.edit(embed=embed)

        except discord.ext.commands.ExtensionNotFound:
            embed = discord.Embed(description=f"<:redTick:596576672149667840> Extension not found")
            
            await message.edit(embed=embed)

        except discord.ext.commands.ExtensionNotLoaded:
            embed = discord.Embed(description=f"<:redTick:596576672149667840> Extension not loaded")
            
            await message.edit(embed=embed)

    @commands.command(
        help="Reloads all cogs",
        aliases=['relall', 'rall', 'reloadall'])
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def reload(self, ctx, *extensions : jishaku.modules.ExtensionConverter):
        pages = WrappedPaginator(prefix='', suffix='')
        to_send = []
        err = False
        first_reload_failed_extensions = []

        extensions = extensions or [await jishaku.modules.ExtensionConverter.convert(self, ctx, '~')]

        for extension in itertools.chain(*extensions):
            method, icon = (
                (self.client.reload_extension, "\N{CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS}")
                if extension in self.client.extensions else
                (self.client.load_extension, "\N{INBOX TRAY}")
            )
            # noinspection PyBroadException
            try:
                method(extension)
                pages.add_line(f"{icon} `{extension}`")
            except Exception:
                first_reload_failed_extensions.append(extension)

        error_keys = {
            discord.ext.commands.ExtensionNotFound: 'Not found',
            discord.ext.commands.NoEntryPointError: 'No setup function',
            discord.ext.commands.ExtensionNotLoaded: 'Not loaded',
            discord.ext.commands.ExtensionAlreadyLoaded: 'Already loaded'
        }

        for extension in first_reload_failed_extensions:
            method, icon = (
                (self.client.reload_extension, "\N{CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS}")
                if extension in self.client.extensions else
                (self.client.load_extension, "\N{INBOX TRAY}")
            )
            try:
                method(extension)
                pages.add_line(f"{icon} `{extension}`")

            except tuple(error_keys.keys()) as exc:
                pages.add_line(f"{icon}<:redTick:596576672149667840> `{extension}` - {error_keys[type(exc)]}")

            except discord.ext.commands.ExtensionFailed as e:
                traceback_string = f"```py" \
                                   f"\n{''.join(traceback.format_exception(etype=None, value=e, tb=e.__traceback__))}" \
                                   f"\n```"
                pages.add_line(f"{icon}<:redTick:596576672149667840> `{extension}` - Execution error")
                to_dm = f"<:redTick:596576672149667840> {extension} - Execution error - Traceback:"

                if (len(to_dm) + len(traceback_string) + 5) > 2000:
                    await ctx.author.send(file=io.StringIO(traceback_string))
                else:
                    await ctx.author.send(f"{to_dm}\n{traceback_string}")

        for page in pages.pages:
            await ctx.send(page)

    @commands.command(
        help="Reloads one or multiple cogs",
        aliases=['mload', 'mrl'])
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    @commands.is_owner()
    async def mreload(self, ctx, *extensions : jishaku.modules.ExtensionConverter):
        pages = WrappedPaginator(prefix='', suffix='')

        if not extensions:
            extensions = [await jishaku.modules.ExtensionConverter.convert(self, ctx, 'helper')]

        for extension in itertools.chain(*extensions):
            method, icon = (
                (None, "\N{CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS}")
            )

            try:
                module = importlib.import_module(extension)
                importlib.reload(module)

            except Exception as exc:  # pylint: disable=broad-except
                traceback_data = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__, 1))

                pages.add_line(
                    f"{icon}\N{WARNING SIGN} `{extension}`\n```py\n{traceback_data}\n```",
                    empty=True
                )
            else:
                pages.add_line(f"{icon} `{extension}`")

        for page in pages.pages:
            await ctx.send(page)
 
        
    @commands.command(
        help="Shutdowns the bot",
        aliases=['shutdown_bot'])
    @commands.is_owner()
    async def shutdown(self, ctx):
        message = await ctx.send("Shutting down...")
        
        asyncio.sleep(0.5)
        
        await message.edit("Goodbye!")
        
        os.system('sudo systemctl stop stealthbot')
        
    @commands.command(help="Restarts the bot",
                      aliases=['reload_bot'])
    @commands.is_owner()
    async def restart_bot(self, ctx):
        embed = discord.Embed(title="Restarting...")
        
        message = await ctx.send(embed=embed)
        
        asyncio.sleep(0.5)
        
        os.system('sudo systemctl restart stealthbot')

    @commands.command(
        help="Pulls code from github and reloads all files",
        aliases=['pull', 'githubpull', 'github_pull'])
    @commands.is_owner()
    async def update(self, ctx):
        start1 = time.perf_counter()
        
        cmd = self.client.get_command("jsk git")
        await ctx.invoke(cmd, argument=jishaku.codeblocks.codeblock_converter("pull")) 
        
        end1 = time.perf_counter()
        
        pullMs = (end1 - start1) * 1000
        
        start2 = time.perf_counter()
        
        cmd = self.client.get_command("rall")
        await ctx.invoke(cmd)
        
        end2 = time.perf_counter()
        
        rallMs = (end2 - start2) * 1000
    
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
                
        embed = discord.Embed(title="Done updating bot!", description=f"""
`jsk git pull` took {round(pullMs)}ms{' ' * (9-len(str(round(pullMs, 3))))}
`rall channel` took {round(rallMs)}ms{' ' * (9-len(str(round(rallMs, 3))))}
                              """)
        
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.is_owner()
    async def enable(self, ctx, command : str):
        command = self.client.get_command(command)
        if command.enabled:
            return await ctx.send(f"`{command}` is already enabled.")
        command.enabled = True
        await ctx.send(f"Successfully enabled the `{command.name}` command.")
        
    @commands.command()
    @commands.is_owner()
    async def disable(self, ctx, command : str):
        command = self.client.get_command(command)
        if not command.enabled:
            return await ctx.send(f"`{command}` is already disabled.")
        command.enabled = False
        await ctx.send(f"Successfully disabled the `{command.name}` command.")

    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, *, message):
        await ctx.send(message)
        
    @commands.command()
    @commands.is_owner()
    async def spam(self, ctx, number, channel : discord.TextChannel, *, message):
        try:
            await ctx.message.delete()
        except:
            pass
        number = range(int(number))
        for i in number:
            await channel.send(message)

    @commands.command(help="Toggles the no-prefix mode on/off", aliases=["no_prefix", "silentprefix", "silent_prefix"])
    @commands.is_owner()
    async def noprefix(self, ctx, state : str=None):
        if state == 'on':
            await ctx.message.add_reaction('<:toggle_on:857842924729270282>')
            self.client.no_prefix = True
        elif state == 'off':
            await ctx.message.add_reaction('<:toggle_off:857842924544065536>')
            self.client.no_prefix = False
        else:
            if self.client.no_prefix == False:
                await ctx.message.add_reaction('<:toggle_on:857842924729270282>')
                self.client.no_prefix = True
            elif self.client.no_prefix == True:
                await ctx.message.add_reaction('<:toggle_off:857842924544065536>')
                self.client.no_prefix = False

    @commands.command(help="Toggles the bot-maintenance mode on/off", aliases=["bot_maintenance", "maintenancebot", "maintenance_bot", 'botmaintenance'])
    @commands.is_owner()
    async def maintenance(self, ctx, state : str=None):
        if state == 'on':
            await ctx.message.add_reaction('<:toggle_on:857842924729270282>')
            self.client.maintenance = True
        elif state == 'off':
            await ctx.message.add_reaction('<:toggle_off:857842924544065536>')
            self.client.maintenance = False
        else:
            if self.client.maintenance == False:
                await ctx.message.add_reaction('<:toggle_on:857842924729270282>')
                self.client.maintenance = True
            elif self.client.maintenance == True:
                await ctx.message.add_reaction('<:toggle_off:857842924544065536>')
                self.client.maintenance = False


    # @commands.command(help="Loads a cog", aliases=['le', 'lc', 'loadcog'])
    # @commands.is_owner()
    # async def load(self, ctx, extension):
    #     embed = discord.Embed(description=f"<a:loading:747680523459231834> Loading {extension}...")
    #     embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #     message = await ctx.send(embed=embed)

    #     try:
    #         self.client.load_extension(f"cogs.{extension}")
    #         embed = discord.Embed(description=f":white_check_mark: {extension}", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         await message.edit(embed=embed)

    #     except discord.ext.commands.ExtensionNotFound:
    #         embed = discord.Embed(description=":x: That cog doesn't exist.", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         await message.edit(embed=embed)

    #     except discord.ext.commands.ExtensionAlreadyLoaded:
    #         embed = discord.Embed(description=":x: That cog is already loaded.", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         await message.edit(embed=embed)

    #     except discord.ext.commands.NoEntryPointError:
    #         embed = discord.Embed(description=":x: That cog doesn't have a setup function.", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         await message.edit(embed=embed)

    #     except discord.ext.commands.ExtensionFailed as e:
    #         traceback_string = "".join(traceback.format_exception(etype=None, value=e, tb=e.__traceback__))
    #         embed = discord.Embed(description=":x An error occurred while trying to load that cog.\n```{traceback_string}```", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         try:
    #             await message.edit(embed=embed)

    #         except:
    #             embed = discord.Embed(description=":x: An error occurred while trying to load that cog. ```\nError message is too long to send it here.\nPlease check the console\n```", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #             embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #             await message.edit()
    #         raise e

    # @commands.command(help="Unloads a cog", aliases=['unl', 'ue', 'uc'])
    # @commands.is_owner()
    # async def unload(self, ctx, extension):
    #     embed = discord.Embed(description=f"⬇ {extension}", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #     message = await ctx.send(embed=embed)

    #     try:
    #         self.client.unload_extension("cogs.{}".format(extension))
    #         embed = discord.Embed(description=f":white_check_mark: {extension}", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         await message.edit(embed=embed)

    #     except discord.ext.commands.ExtensionNotFound:
    #         embed = discord.Embed(description=f":x: That cog doesn't exist.", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         await message.edit(embed=embed)

    #     except discord.ext.commands.ExtensionNotLoaded:
    #         embed = discord.Embed(description = f":x: That cog isn't loaded.", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         await message.edit(embed=embed)

    # @commands.command(help="Reloads an cog", aliases=['rel', 'rc'])
    # @commands.is_owner()
    # async def reload(self, ctx, extension):
    #     embed = discord.Embed(description=f"<a:loading:747680523459231834> {extension}", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #     message = await ctx.send(embed=embed)

    #     try:
    #         self.client.reload_extension("cogs.{}".format(extension))
    #         embed = discord.Embed(description=f":white_check_mark: {extension}", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         await message.edit(embed=embed)

    #     except discord.ext.commands.ExtensionNotLoaded:
    #         embed = discord.Embed(description=":x: That cog isn't loaded.", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         await message.edit(embed=embed)

    #     except discord.ext.commands.ExtensionNotFound:
    #         embed = discord.Embed(description=":x: That cog doesn't exist.", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         await message.edit(embed=embed)

    #     except discord.ext.commands.NoEntryPointError:
    #         embed = discord.Embed(description="x: That cog doesn't have a setup function", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         await message.edit(embed=embed)

    #     except discord.ext.commands.ExtensionFailed as e:
    #         traceback_string = "".join(traceback.format_exception(etype=None, value=e, tb=e.__traceback__))
    #         embed = discord.Embed(description = f":x: An error occurred while trying to load that cog.\n```{traceback_string}```", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #         embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #         try:
    #             await message.edit(embed=embed)

    #         except:
    #             embed = discord.Embed(description = f"An error occurred while trying to load that cog.\n``` error too long, check the console\n```", timestamp=discord.utils.utcnow(), color=0x2F3136)
    #             embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    #             await message.edit()
    #         raise e

    # @commands.command(help="Reloads all cogs", aliases=['relall', 'rall'])
    # @commands.is_owner()
    # async def reloadall(self, ctx, argument: typing.Optional[str]):
    #     list = ""
    #     desc = ""
    #     err = False
    #     rerel = []
    #     if argument == 'silent' or argument == 's': silent = True
    #     else: silent = False
    #     if argument == 'channel' or argument == 'c': channel = True
    #     else: channel = False

    #     for filename in os.listdir("./cogs"):
    #         if filename.endswith(".py"):
    #             list = f"{list} \n🔃 {filename[:-3]}"

    #     embed = discord.Embed(description=list)
        
    #     message = await ctx.send(embed=embed)

    #     for filename in os.listdir("./cogs"):
    #         if filename.endswith(".py"):
    #             try:
    #                 self.client.reload_extension("cogs.{}".format(filename[:-3]))
    #                 desc = f"{desc} \n✅ {filename[:-3]}"
    #             except:
    #                 rerel.append(filename)

    #     for filename in rerel:
    #         try:
    #             self.client.reload_extension("cogs.{}".format(filename[:-3]))
    #             desc = f"{desc} \n✅ {filename[:-3]}"

    #         except discord.ext.commands.ExtensionNotLoaded:
    #             desc = f"{desc} \n❌ {filename[:-3]} - Not loaded"
    #         except discord.ext.commands.ExtensionNotFound:
    #             desc = f"{desc} \n❌ {filename[:-3]} - Not found"
    #         except discord.ext.commands.NoEntryPointError:
    #             desc = f"{desc} \n❌ {filename[:-3]} - No setup function"
    #         except discord.ext.commands.ExtensionFailed as e:
    #             traceback_string = "".join(traceback.format_exception(etype=None, value=e, tb=e.__traceback__))
    #             desc = f"{desc} \n❌ {filename[:-3]} - Execution error"
    #             embederr = discord.Embed(description=f"\n❌ {filename[:-3]} Execution error - Traceback\n```\n{traceback_string}\n```")
    #             if silent == False:
    #                 if channel == False: await ctx.author.send(embed=embederr)
    #                 else: await ctx.send(embed=embederr)
    #             err = True

    #     if err == True:
    #         if silent == False:
    #             if channel == False: desc = f"{desc} \n\n📬 {ctx.author.mention}, I sent you all the tracebacks."
    #             else: desc = f"{desc} \n\n📬 Sent all tracebacks here."
    #         if silent == True: desc = f"{desc} \n\n📭 silent, no tracebacks sent."
    #         embed = discord.Embed(title="Reloaded some cogs", description=desc)
            
    #         await message.edit(embed=embed)
            
    #     else:
    #         embed = discord.Embed(title="Reloaded all extensions", description=desc)
            
    #         await message.edit(embed=embed)
    
    @commands.group(invoke_without_command=True, help="Blacklist command", aliases=['bl'])
    @commands.is_owner()
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send("youre so retarded")
        
    @commands.group(aliases=['to_do'])
    @commands.is_owner()
    async def todo(self, ctx):
        return await ctx.send("no?")
        
    @todo.command(name="add", help="Adds a todo to your todo list", aliases=['a'])
    async def todo_add(self, ctx, number : int, text : str):
        await self.client.db.execute("INSERT INTO todo (number, text, creation_date) VALUES ($1, $2, $3) "
                                    "ON CONFLICT (text) DO UPDATE SET creation_date = $3",
                                    number, text[0:1800], ctx.message.created_at)
        
        embed = discord.Embed(description=f"Successfully added `{text[0:1800]}` to your todo list. (Number: `{number}`)")

        await ctx.send(embed=embed)
        
    @todo.command(name="remove", help="Remove a todo from your todo list", aliases=['r', 'rm'])
    async def todo_remove(self, ctx, number : int):
        await self.client.db.execute("DELETE FROM todo where number = $1",
                                    number)
        
        embed = discord.Embed(description=f"Successfully removed `{number}` from your todo list")

        await ctx.send(embed=embed)

    @blacklist.command(name="add", help="Adds a member to the blacklist", aliases=['a'])
    async def blacklist_add(self, ctx, member : discord.User, *, reason : str):

        await self.client.db.execute(
            "INSERT INTO blacklist(user_id, is_blacklisted, reason) VALUES ($1, $2, $3) "
            "ON CONFLICT (user_id) DO UPDATE SET is_blacklisted = $2",
            member.id, True, reason[0:1800])

        self.client.blacklist[member.id] = True

        embed = discord.Embed(description=f"Successfully added {member} to the blacklist with the reason being {reason[0:1800]}", timestamp=discord.utils.utcnow(), color=0x2F3136)

        return await ctx.send(embed=embed)

    @blacklist.command(name="remove", help="Removes a member from the blacklist", aliases=['r', 'rm'])
    async def blacklist_remove(self, ctx, member : discord.User):

        await self.client.db.execute(
            "DELETE FROM blacklist where user_id = $1",
            member.id)

        self.client.blacklist[member.id] = False

        embed = discord.Embed(description=f"Successfully removed {member} from the blacklist", timestamp=discord.utils.utcnow(), color=0x2F3136)

        return await ctx.send(embed=embed)

    @blacklist.command(name='check', help="Checks if a member is blacklisted", aliases=['c'])
    async def blacklist_check(self, ctx, member : discord.User):
        try:
            status = self.client.blacklist[member.id]

        except KeyError:
            status = False
            
        if status is True:
            reason = await self.client.db.fetchval("SELECT reason FROM todo WHERE user_id = $1", member.id)
            text = f"{member} is blacklisted\nReason: {reason}"
            
        embed = discord.Embed(description=f"{text}", timestamp=discord.utils.utcnow(), color=0x2F3136)

        return await ctx.send(embed=embed)

    @blacklist.command(name='list', help="Sends a list of banned members", aliases=['l'])
    async def blacklist_list(self, ctx):
        blacklistedUsers = []
        
        blacklist = await self.client.db.fetch("SELECT * FROM blacklist")
        for stuff in blacklist:
            user = self.client.get_user(stuff["user_id"])
            reason = stuff["reason"]
            
            blacklistedUsers.append(f"{user.name} **|** {user.id} **|** [Hover over for reason]({ctx.message.jump_url} '{reason}')")
            
        paginator = ViewMenuPages(source=BlacklitedUsersEmbedPage(blacklistedUsers), clear_reactions_after=True)
        page = await paginator._source.get_page(0)
        kwargs = await paginator._get_kwargs_from_page(page)
        if paginator.build_view():
            paginator.message = await ctx.send(embed=kwargs['embed'],view = paginator.build_view())
        else:
            paginator.message = await ctx.send(embed=kwargs['embed'])
        await paginator.start(ctx)
