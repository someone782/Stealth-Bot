import discord
import helpers
import datetime
import asyncio
import os
import typing
import time
import traceback
import errors
import jishaku
import random
from discord.ext import commands

def setup(client):
    client.add_cog(Owner(client))

class Owner(commands.Cog):
    "<:owner_crown:845946530452209734> | Commands that only the developer of this client can use"
    def __init__(self, client):
        self.hidden = True
        self.client = client
        
        async def say_permissions(self, ctx, member):
            permissions = [perm for perm in member.guild_permissions]
            e = discord.Embed(colour=member.colour)
            e.set_author(name=f'Showing Permissions For {member}')
            allowed, denied = [], []
            for name, value in permissions:
                name = name.replace('_', ' ').replace('guild', 'server').title()
                if value:
                    allowed.append(f'**+** {name}')
                else:
                    denied.append(f'**-** {name}')

            if '**+** Administrator' in allowed:
                allowed = ['**+** Administrator']
            if len(denied) == 0:
                denied = ['**-** None']
            
            e.add_field(name='<a:Yes:889079191566422027> Allowed:',value='\n'.join(allowed))
            e.add_field(name='<a:No:889079913498415134> Denied:',value='\n'.join(denied))
            await ctx.send(embed=e)
        
    @commands.command(help="Shutdowns the bot", aliases=['shutdown_bot'])
    @commands.is_owner()
    async def shutdown(self, ctx):
        message = await ctx.send("Shutting down...")
        
        asyncio.sleep(0.5)
        
        await message.edit("Goodbye!")
        
        os.system('sudo systemctl stop stealthbot')
        
    @commands.command(help="Restarts the bot")
    @commands.is_owner()
    async def restart_bot(self, ctx):
        embed = discord.Embed(title="Restarting...")
        
        message = await ctx.send(embed=embed)
        
        asyncio.sleep(0.5)
        
        os.system('sudo systemctl restart stealthbot')

    @commands.command(help="Pulls code from github and reloads all files", aliases=['pull', 'githubpull', 'github_pull'])
    @commands.is_owner()
    async def update(self, ctx):
        start1 = time.perf_counter()
        
        cmd = self.client.get_command("jsk git")
        await ctx.invoke(cmd, argument=jishaku.codeblocks.codeblock_converter("pull")) 
        
        end1 = time.perf_counter()
        
        pullMs = (end1 - start1) * 1000
        
        start2 = time.perf_counter()
        
        cmd = self.client.get_command("rall")
        await ctx.invoke(cmd, argument="channel")
        
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
    @commands.guild_only()
    async def wtf(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        await self.say_permissions(ctx, member)
            
    @commands.command(help="Shows you what permissions the bot has in the current server", aliases=['permissions', 'botperms', 'bot_perms', 'botpermissions', 'bot_permissions'])
    async def perms(self, ctx):
        allowed = "\n <a:Yes:889079191566422027> ".join(permission.replace("_", " ").title() for permission, value in ctx.guild.me.guild_permissions if value)
        notAllowed = "\n <a:No:889079913498415134> ".join(permission.replace("_", " ").title() for permission, value in ctx.guild.me.guild_permissions if not value)
        
        embed = discord.Embed(title="Bot permissions")
        embed.add_field(name="Allowed", value=f"<a:Yes:889079191566422027> {allowed}", inline=True)
        embed.add_field(name="Denied", value=f"<a:No:889079913498415134> {notAllowed}", inline=True)
                        
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

    @commands.command(aliases=['borgor', 'burgor'])
    async def burger(self, ctx):
        raise errors.KillYourself

    @commands.command(aliases=['to_do'])
    @commands.is_owner()
    async def todo(self, ctx, *, text):
        channel = self.client.get_channel(881541529381007431)

        await channel.send(f"TO DO: {text}")

        embed = discord.Embed(title=f"Sent to do!", description=f"What was sent: {text}", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(help="toggles no-prefix mode on or off", aliases=["no_prefix", "silentprefix", "silent_prefix"])
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


    @commands.command(help="Loads a cog", aliases=['le', 'lc', 'loadcog'])
    @commands.is_owner()
    async def load(self, ctx, extension):
        embed = discord.Embed(description=f"<a:loading:747680523459231834> Loading {extension}...")
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        message = await ctx.send(embed=embed)

        try:
            self.client.load_extension(f"cogs.{extension}")
            embed = discord.Embed(description=f":white_check_mark: {extension}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

        except discord.ext.commands.ExtensionNotFound:
            embed = discord.Embed(description=":x: That cog doesn't exist.", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

        except discord.ext.commands.ExtensionAlreadyLoaded:
            embed = discord.Embed(description=":x: That cog is already loaded.", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

        except discord.ext.commands.NoEntryPointError:
            embed = discord.Embed(description=":x: That cog doesn't have a setup function.", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

        except discord.ext.commands.ExtensionFailed as e:
            traceback_string = "".join(traceback.format_exception(etype=None, value=e, tb=e.__traceback__))
            embed = discord.Embed(description=":x An error occurred while trying to load that cog.\n```{traceback_string}```", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            try:
                await message.edit(embed=embed)

            except:
                embed = discord.Embed(description=":x: An error occurred while trying to load that cog. ```\nError message is too long to send it here.\nPlease check the console\n```", timestamp=discord.utils.utcnow(), color=0x2F3136)
                embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

                await message.edit()
            raise e

    @commands.command(help="Unloads a cog", aliases=['unl', 'ue', 'uc'])
    @commands.is_owner()
    async def unload(self, ctx, extension):
        embed = discord.Embed(description=f"⬇ {extension}", timestamp=discord.utils.utcnow(), color=0x2F3136)
        message = await ctx.send(embed=embed)

        try:
            self.client.unload_extension("cogs.{}".format(extension))
            embed = discord.Embed(description=f":white_check_mark: {extension}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

        except discord.ext.commands.ExtensionNotFound:
            embed = discord.Embed(description=f":x: That cog doesn't exist.", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

        except discord.ext.commands.ExtensionNotLoaded:
            embed = discord.Embed(description = f":x: That cog isn't loaded.", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

    @commands.command(help="Reloads an cog", aliases=['rel', 'rc'])
    @commands.is_owner()
    async def reload(self, ctx, extension):
        embed = discord.Embed(description=f"<a:loading:747680523459231834> {extension}", timestamp=discord.utils.utcnow(), color=0x2F3136)
        message = await ctx.send(embed=embed)

        try:
            self.client.reload_extension("cogs.{}".format(extension))
            embed = discord.Embed(description=f":white_check_mark: {extension}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

        except discord.ext.commands.ExtensionNotLoaded:
            embed = discord.Embed(description=":x: That cog isn't loaded.", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

        except discord.ext.commands.ExtensionNotFound:
            embed = discord.Embed(description=":x: That cog doesn't exist.", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

        except discord.ext.commands.NoEntryPointError:
            embed = discord.Embed(description="x: That cog doesn't have a setup function", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

        except discord.ext.commands.ExtensionFailed as e:
            traceback_string = "".join(traceback.format_exception(etype=None, value=e, tb=e.__traceback__))
            embed = discord.Embed(description = f":x: An error occurred while trying to load that cog.\n```{traceback_string}```", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            try:
                await message.edit(embed=embed)

            except:
                embed = discord.Embed(description = f"An error occurred while trying to load that cog.\n``` error too long, check the console\n```", timestamp=discord.utils.utcnow(), color=0x2F3136)
                embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

                await message.edit()
            raise e

    @commands.command(help="Reloads all cogs", aliases=['relall', 'rall'])
    @commands.is_owner()
    async def reloadall(self, ctx, argument: typing.Optional[str]):
        list = ""
        desc = ""
        err = False
        rerel = []
        if argument == 'silent' or argument == 's': silent = True
        else: silent = False
        if argument == 'channel' or argument == 'c': channel = True
        else: channel = False

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                list = f"{list} \n🔃 {filename[:-3]}"

        embed = discord.Embed(description=list)
        
        message = await ctx.send(embed=embed)

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    self.client.reload_extension("cogs.{}".format(filename[:-3]))
                    desc = f"{desc} \n✅ {filename[:-3]}"
                except:
                    rerel.append(filename)

        for filename in rerel:
            try:
                self.client.reload_extension("cogs.{}".format(filename[:-3]))
                desc = f"{desc} \n✅ {filename[:-3]}"

            except discord.ext.commands.ExtensionNotLoaded:
                desc = f"{desc} \n❌ {filename[:-3]} - Not loaded"
            except discord.ext.commands.ExtensionNotFound:
                desc = f"{desc} \n❌ {filename[:-3]} - Not found"
            except discord.ext.commands.NoEntryPointError:
                desc = f"{desc} \n❌ {filename[:-3]} - No setup function"
            except discord.ext.commands.ExtensionFailed as e:
                traceback_string = "".join(traceback.format_exception(etype=None, value=e, tb=e.__traceback__))
                desc = f"{desc} \n❌ {filename[:-3]} - Execution error"
                embederr = discord.Embed(description=f"\n❌ {filename[:-3]} Execution error - Traceback\n```\n{traceback_string}\n```")
                if silent == False:
                    if channel == False: await ctx.author.send(embed=embederr)
                    else: await ctx.send(embed=embederr)
                err = True

        if err == True:
            if silent == False:
                if channel == False: desc = f"{desc} \n\n📬 {ctx.author.mention}, I sent you all the tracebacks."
                else: desc = f"{desc} \n\n📬 Sent all tracebacks here."
            if silent == True: desc = f"{desc} \n\n📭 silent, no tracebacks sent."
            embed = discord.Embed(title="Reloaded some cogs", description=desc)
            
            await message.edit(embed=embed)
            
        else:
            embed = discord.Embed(title="Reloaded all extensions", description=desc)
            
            await message.edit(embed=embed)

    @commands.group(invoke_without_command=True, help="Blacklist command", aliases=['bl'])
    @commands.is_owner()
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send("youre so retarded")

    @blacklist.command(name="add", help="Adds a member to the blacklist", aliases=['a'])
    async def blacklist_add(self, ctx, member : discord.User):

        await self.client.db.execute(
            "INSERT INTO blacklist(user_id, is_blacklisted) VALUES ($1, $2) "
            "ON CONFLICT (user_id) DO UPDATE SET is_blacklisted = $2",
            member.id, True)

        self.client.blacklist[member.id] = True

        embed = discord.Embed(description=f"Successfully added {member} to the blacklist", timestamp=discord.utils.utcnow(), color=0x2F3136)

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
        embed = discord.Embed(description=f"{member} {'is' if status is True else 'is not'} blacklisted", timestamp=discord.utils.utcnow(), color=0x2F3136)

        return await ctx.send(embed=embed)
