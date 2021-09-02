import discord
import datetime
import io
import asyncio
import random
import helpers
from PIL import Image, ImageSequence
import aiohttp
from discord.ext import commands

class other(commands.Cog):
    "All other commands"
    def __init__(self, client):
        self.client = client
        client.session = aiohttp.ClientSession()

    @commands.command(help="Sends the source code of the bot", aliases=['code', 'sourcecode', 'source_code'])
    async def source(self, ctx):
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, emoji="<:github:744345792172654643>", label="Source Code", url="https://github.com/Ender2K89/Stealth-Bot")
        view.add_item(item=item)

        embed = discord.Embed(title="Click here for the source code of this bot", url="https://github.com/Ender2K89/Stealth-Bot", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed, view=view)

    @commands.command(help="Sends a invite of the bot", alises=['inv', 'invite_me', 'inviteme'])
    async def invite(self, ctx):
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, emoji="<:invite:860644752281436171>", label="Invite me", url="https://discord.com/api/oauth2/authorize?client_id=760179628122964008&permissions=8&scope=bot")
        view.add_item(item=item)

        embed = discord.Embed(title="Click here for the invite to this bot", url="https://discord.com/api/oauth2/authorize?client_id=760179628122964008&permissions=8&scope=bot", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed, view=view)

    @commands.command(help="Sends the support server of the bot", aliases=['supportserver', 'support_server'])
    async def support(self, ctx):
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, emoji="<:servers:870152102759006208>", label="Join support server", url="https://discord.gg/MrBcA6PZPw")
        view.add_item(item=item)

        embed = discord.Embed(title="Click here for the invite to the support server", url="https://discord.gg/MrBcA6PZPw", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed, view=view)

    @commands.command(help="Changes the prefix for the current server", aliases=['pre', 'setprefix', 'set_prefix'])
    @commands.check_any(commands.has_permissions(manage_guild=True), commands.is_owner())
    async def prefix(self, ctx, prefix=None):
        old = await self.client.db.fetchval('SELECT prefix FROM guilds WHERE guild_id = $1', ctx.guild.id)
        if not prefix:
            old = old or 'sb!'
            await ctx.send(f"My prefix in this server is `{old}`.")
            return

        if len(prefix) > 10:
            return await ctx.send("Prefix cannot be more than 10 characters.")
        if not old:
            await self.client.db.execute('INSERT INTO guilds(guild_id, prefix) VALUES ($1, $2)', ctx.guild.id, prefix)
            await ctx.send(f"Changed prefix from `{old}` to `{prefix}`.")
        elif old != prefix:
            await self.client.db.execute('UPDATE guilds SET prefix = $1 WHERE guild_id = $2', prefix, ctx.guild.id)
            await ctx.send(f"Changed prefix from `{old}` to `{prefix}`.")
        else:
            await ctx.send(f"`{prefix}` is already the prefix.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 120, commands.BucketType.user) # Sets the cooldown to 120 seconds for the user executing the command
    async def chat(self, ctx):
        if ctx.guild.id == 799330949686231050:
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
        else:
            embed = discord.Embed(title="You can only use this command in the `Stealth Hangout` server.", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)

    @commands.command(help="Verifies you", hidden=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    @helpers.is_sh_server()
    async def verify(self, ctx):
        with open("./data/verifyWords.txt", "r") as file:
            allText = file.read()
            wordsList = list(map(str, allText.split()))

        member = ctx.author
        role = 'Members'
        correctAnswer = random.choice(wordsList)

        message = await ctx.send(f"Please say `{correctAnswer}` to verify.\nYou have 15 seconds to type the word.")

        def check(m):
            return m.content == correctAnswer and m.channel.id == ctx.channel.id

        try:
            msg = await self.client.wait_for(event='message', check=check, timeout=15)
        except asyncio.TimeoutError:
            await message.delete()
            await ctx.message.delete(delay=5.0)
            await ctx.reply("It's been over 15 seconds, please try again by doing `-verify`", delete_after=5.0)
        else:
            await ctx.message.delete()
            await message.delete()
            await msg.delete(delay=5.0)
            await msg.reply("You've successfully verified!", delete_after=5.0)

            await member.add_roles(discord.utils.get(member.guild.roles, name=role))

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

    @commands.command(help="Sends a screenshot of the site you specify.\nNOTE: It needs to be with http/s.", aliases=['ss', 'screenshot_website', 'ss_website'])
    @commands.is_nsfw()
    async def screenshot(self, ctx, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://image.thum.io/get/width/1920/crop/675/maxAge/1/noanimate/{url}') as r:
                res = await r.read()

        embed = discord.Embed(title=f"Screenshot of {url}", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.set_image(url="attachment://ss.png")

        if "ip" in url.lower() or "test" in url.lower() or "speed" in url.lower() or "address" in url.lower():
            await ctx.reply("no.")
        else:
            await ctx.reply(embed=embed, file=discord.File(io.BytesIO(res), filename="ss.png"))

    @commands.command(help="secret command", hidden=True)
    @commands.is_owner()
    async def bypass_here(self, ctx):
        channel = self.client.get_channel(837348307570393218)
        embed = discord.Embed(title="Welcome to `#bypass_here`!", url="https://discord.gg/5UsKEFKHtH", description="In this channel you're supposed to try to bypass the anti-swear or the anti-invite system.\n\n```diff\n- Misusing this channel will result in a mute\n+ All messages are deleted after a bit\n+ Only ping the owner if you find over 10 bypasses\n```", color=0x2F3136)
        await ctx.message.delete()
        message = await channel.send(embed=embed)
        await message.pin()


    @commands.command(help="Average embed fields enjoyer vs average embed description enjoyer", hidden=True)
    async def embed(self, ctx):
        await ctx.reply("https://cdn.upload.systems/uploads/udt7Bv0U.gif")


def setup(client):
    client.add_cog(other(client))
