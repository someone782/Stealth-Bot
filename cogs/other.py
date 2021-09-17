import discord
import datetime
import io
import asyncio
import random
import helpers
from PIL import Image, ImageSequence
import errors
import aiohttp
from discord.ext import commands

def setup(client):
    client.add_cog(Other(client))

class Other(commands.Cog):
    "❓ All other commands"
    def __init__(self, client):
        self.client = client

    @commands.command(help="Sends a invite of the bot", alises=['inv', 'invite_me', 'inviteme'])
    async def invite(self, ctx):
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, emoji="<:invite:860644752281436171>", label="Invite me", url="https://discord.com/api/oauth2/authorize?client_id=760179628122964008&permissions=8&scope=bot")
        view.add_item(item=item)

        embed = discord.Embed(title="Click here for the invite to this bot", url="https://discord.com/api/oauth2/authorize?client_id=760179628122964008&permissions=8&scope=bot")
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed, view=view)

    @commands.command(help="Sends the support server of the bot", aliases=['supportserver', 'support_server'])
    async def support(self, ctx):
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, emoji="<:servers:870152102759006208>", label="Join support server", url="https://discord.gg/MrBcA6PZPw")
        view.add_item(item=item)

        embed = discord.Embed(title="Click here for the invite to the support server", url="https://discord.gg/MrBcA6PZPw")
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed, view=view)

    @commands.group(invoke_without_command=True, help="Shows you a list of the bot's prefixes", aliases=['prefix'])
    async def prefixes(self, ctx):
        prefixes = await self.client.get_pre(self.client, ctx.message, raw_prefix=True)
        embed = discord.Embed(title="Here's a list of my prefixes for this server:", description=ctx.me.mention + '\n' + '\n'.join(prefixes))
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        return await ctx.send(embed=embed)

    @commands.check_any(commands.has_permissions(manage_guild=True), commands.is_owner())
    @prefixes.command(name="add", help="Adds a prefix to the bot's prefixes (To add a prefix with a space put quotation marks around it)", aliases=['a', 'create'])
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
    @prefixes.command(name="remove", help="Removes a prefix from the bot's prefixes (To remove a prefix with a space put quotation marks around it)", aliases=['r', 'delete'])
    async def prefixes_remove(self, ctx, prefix : str):
        old = list(await self.client.get_pre(self.client, ctx.message, raw_prefix=True))

        if prefix in old:
            old.remove(prefix)
            await self.client.db.execute(
                "INSERT INTO guilds(guild_id, prefix) VALUES ($1, $2) "
                "ON CONFLICT (guild_id) DO UPDATE SET prefix = $2",
                ctx.guild.id, old)

            self.client.prefixes[ctx.guild.id] = old

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
            embed = discord.Embed(title="You can only use this command in the `Stealth Hangout` server.")
            embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

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
            await ctx.message.delete(delete_after=5.0) # Deletes the author's message | -verify
            await message.delete() # Deletes the bot's message | Please say ... to verify
            await msg.delete() # Delete the member's answer
            await ctx.reply("You've successfully verified!", delete_after=5.0)

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
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)

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

    @commands.command(help="Sends a screenshot of the site you specify.\nNOTE: It needs to be with http/s.", aliases=['ss', 'screenshot_website', 'ss_website'])
    @commands.is_nsfw()
    async def screenshot(self, ctx, url):
        #async with self.client.session() as session:
        async with self.client.session.get(f'https://image.thum.io/get/width/1920/crop/675/maxAge/1/noanimate/{url}') as r:
            res = await r.read()

        embed = discord.Embed(title=f"Screenshot of {url}")
        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.set_image(url="attachment://ss.png")

        if "ip" in url.lower() or "test" in url.lower() or "speed" in url.lower() or "address" in url.lower():
            await ctx.send("no.")
        else:
            await ctx.send(embed=embed, file=discord.File(io.BytesIO(res), filename="ss.png"))

    @commands.command(help="secret command", hidden=True)
    @commands.is_owner()
    async def bypass_here(self, ctx):
        channel = self.client.get_channel(837348307570393218)
        embed = discord.Embed(title="Welcome to `#bypass_here`!", url="https://discord.gg/5UsKEFKHtH", description="In this channel you're supposed to try to bypass the anti-swear or the anti-invite system.\n\n```diff\n- Misusing this channel will result in a mute\n+ All messages are deleted after a bit\n+ Only ping the owner if you find over 10 bypasses\n```")
        await ctx.message.delete()
        message = await channel.send(embed=embed)
        await message.pin()


    @commands.command(help="Average embed fields enjoyer vs average embed description enjoyer", hidden=True)
    async def embed(self, ctx):
        await ctx.send("https://cdn.upload.systems/uploads/udt7Bv0U.gif")

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