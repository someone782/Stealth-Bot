import discord
import datetime
import io
import helpers
import aiohttp
from discord.ext import commands

class other(commands.Cog):
    "All other commands"
    def __init__(self, client):
        self.client = client

    @commands.command(help="Sends the source code of the bot", aliases=['code', 'sourcecode', 'source_code'])
    async def source(self, ctx):
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, emoji="<:github:744345792172654643>", label="Source Code", url="https://github.com/Ender2K89/Stealth-Bot-Source")
        view.add_item(item=item)

        embed = discord.Embed(title="Click here for the source code of this bot", url="https://github.com/Ender2K89/Stealth-Bot-Source", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed, view=view, mention_author=False)

    @commands.command(help="Sends a invite of the bot", alises=['inv', 'invite_me', 'inviteme'])
    async def invite(self, ctx):
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, emoji="<:invite:860644752281436171>", label="Invite me", url="https://discord.com/api/oauth2/authorize?client_id=760179628122964008&permissions=8&scope=bot")
        view.add_item(item=item)

        embed = discord.Embed(title="Click here for the invite to this bot", url="https://discord.com/api/oauth2/authorize?client_id=760179628122964008&permissions=8&scope=bot", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed, view=view, mention_author=False)

    @commands.command(help="Sends the support server of the bot", aliases=['supportserver', 'support_server'])
    async def support(self, ctx):
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, emoji="<:servers:870152102759006208>", label="Join support server", url="https://discord.gg/MrBcA6PZPw")
        view.add_item(item=item)

        embed = discord.Embed(title="Click here for the invite to the support server", url="https://discord.gg/MrBcA6PZPw", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed, view=view, mention_author=False)

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
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(pass_context=True, help="Verifies you")
    @commands.cooldown(1, 99999999999, commands.BucketType.user) # Sets the cooldown to 99999999999 seconds for the user executing the command
    async def verify(self, ctx):
        user = ctx.message.author
        role = 'Members'
        success_message = 'Verified!'
        try:
            await user.add_roles(discord.utils.get(user.guild.roles, name=role))
            await ctx.message.delete()
            await ctx.send(success_message, delete_after=5.0)
            embed = discord.Embed(title="Someone has verified!", color=0x2F3136)
            embed.add_field(name="Person who verified:", value=f"{user.name}")
            channel = self.client.get_channel(836232733126426666)
            await channel.send(embed=embed)
        except Exception as e:
            await ctx.send('Cannot assign role. Error: ' + str(e))

    @commands.command(aliases=['giveaway_ping', 'ping_giveaway'], help="Pings the Giveaways role")
    @commands.has_role("Staff")
    @commands.cooldown(1, 60, commands.BucketType.user) # Sets the cooldown to 60 seconds for the user executing the command
    async def gping(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"<@&868823472304971817>\n*ping from {ctx.author.mention}*")

    @commands.command(aliases=['qotd_ping', 'ping_qotd'], help="Pings the QOTD role")
    @commands.has_role("Staff")
    @commands.cooldown(1, 60, commands.BucketType.user) # Sets the cooldown to 60 seconds for the user executing the command
    async def qping(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"<@&836281279934496770>\n*ping from {ctx.author.mention}*")

    @commands.command(help="Sends a screenshot of the site you specify.\nNOTE: It needs to be with https.", aliases=['ss', 'screenshot_website', 'ss_website'])
    @commands.is_nsfw()
    async def screenshot(self, ctx, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://image.thum.io/get/width/1920/crop/675/maxAge/1/noanimate/{url}') as r:
                res = await r.read()

        embed = discord.Embed(title=f"Screenshot of {url}", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.set_image(url="attachment://ss.png")

        if "ip" in url.lower():
            await ctx.reply("no.")
        else:
            await ctx.reply(embed=embed, mention_author=False, file=discord.File(io.BytesIO(res), filename="ss.png"))

    @commands.command(help="secret command")
    @commands.is_owner()
    async def bypass_here(self, ctx):
        channel = self.client.get_channel(837348307570393218)
        embed = discord.Embed(title="Welcome to `#bypass_here`!", url="https://discord.gg/5UsKEFKHtH", description="In this channel you're supposed to try to bypass the anti-swear or the anti-invite system.\n\n```diff\n- Misusing this channel will result in a mute\n+ All messages are deleted after a bit\n+ Only ping the owner if you find over 10 bypasses\n```", color=0x2F3136)
        await ctx.message.delete()
        message = await channel.send(embed=embed)
        await message.pin()

    @commands.command()
    async def boobs(self, ctx):
        embed = discord.Embed(title="Click here for boobs", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        await ctx.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(other(client))
