import discord
import datetime
import io
import asyncio
import random
import helpers.helpers as helpers
from PIL import Image, ImageSequence
import re
import errors
import aiohttp
from discord.ext import commands
import emoji

def setup(client):
    client.add_cog(Misc(client))
    
emojis = emoji.unicode_codes.EMOJI_UNICODE["en"].values()

class EmojiConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, arg: str):
        # Discord throws variation selectors on the end sometimes. Just remove it I guess
        if arg.rstrip("\N{variation selector-16}") in emojis or arg in emojis:
            return discord.PartialEmoji(name=arg)
        else:
            raise commands.BadArgument(f"{arg} is not an emoji")

class Misc(commands.Cog):
    ":gear: | Miscellaneous commands"
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def brehj(self, ctx, *args: EmojiConverter):
        await ctx.send(str(args))
        
    @commands.command()
    async def emoji(self, ctx, emoji : discord.PartialEmoji):
        if emoji.animated == True:
            text = f"<a:{emoji.name}:{emoji.id}>"
        else:
            text = f"<:{emoji.name}:{emoji.id}>"
            
        embed = discord.Embed(description=text)
        
        await ctx.send(embed=embed)
        
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