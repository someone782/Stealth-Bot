from aiohttp import helpers
import discord
import random
import helpers
import asyncio
import io
from asyncdagpi import Client, ImageFeatures
import datetime
import aiohttp
import pyfiglet
from discord.ext import commands

class fun(commands.Cog):
    ":zany_face: Fun commands like -meme, -hug and more"
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['guess_the_number'])
    async def number(self, ctx):
        number = random.randint(1, 3)
        await ctx.send(number)
        message = await ctx.reply("Try to guess the number! You have 15 seconds.")

        def check(m):
            return m.content == number and m.channel.id == ctx.channel.id

        try:
            msg = await self.client.wait_for(event='message', check=check, timeout=15)
        except asyncio.TimeoutError:
            await message.delete()
            await ctx.message.delete(delay=5.0)
            await ctx.reply("You lost! It's been 15 seconds and you haven't guessed the number correctly.", delete_after=5.0)
        else:
            await ctx.message.delete()
            await message.delete()
            await msg.delete(delay=5.0)
            await msg.reply("You've got the number right!", delete_after=5.0)

    @commands.command(aliases=['asciitext', 'ascii_text', 'gen_ascii', 'generator_ascii'], description="Turns any text into ASCII")
    async def ascii(self, ctx, *, text):
        ascii = pyfiglet.figlet_format(text)

        embed = discord.Embed(title="ASCII", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.add_field(name="Original text", value=f"{text}")
        embed.add_field(name="ASCII text", value=f"```\n{ascii}\n```")

        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    @commands.command(description="Sends a image of the member you mention but triggered")
    async def triggered(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar.with_format("png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "triggered.gif")
                    embed = discord.Embed(title=f"<a:loading:747680523459231834> Processing image...", timestamp=discord.utils.utcnow(), color=0x2F3136)
                    embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
                    message = await ctx.reply(embed=embed, file=file)
                    embed = discord.Embed(title=f"{member.name} is triggered", timestamp=discord.utils.utcnow(), color=0x2F3136)
                    embed.set_image(url="attachment://triggered.gif")

                    embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
                    await message.edit(content="Image processed!", embed=embed)

    @commands.command(description="Gives the member you mentioned a license to be horny", aliases=['horny_license', 'license_horny'])
    async def horny(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/horny?avatar={member.avatar.with_format("png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")
                    embed = discord.Embed(title=f"<a:loading:747680523459231834> Processing image...", timestamp=discord.utils.utcnow(), color=0x2F3136)
                    embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
                    message = await ctx.reply(embed=embed, file=file)
                    embed = discord.Embed(title=f"{member.name} has the license to be horny", timestamp=discord.utils.utcnow(), color=0x2F3136)
                    embed.set_image(url="attachment://horny.png")

                    embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
                    await message.edit(content="Image processed!", embed=embed)

    @commands.command(description="Gives the member you mentioned a license to be horny", aliases=['go_to_jail', 'in_jail'])
    async def jail(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/jail?avatar={member.avatar.with_format("png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "jail.png")
                    embed = discord.Embed(title=f"<a:loading:747680523459231834> Processing image...", timestamp=discord.utils.utcnow(), color=0x2F3136)
                    embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
                    message = await ctx.reply(embed=embed, file=file)
                    embed = discord.Embed(title=f"{member.name} has been sent to jail for 69420 years", timestamp=discord.utils.utcnow(), color=0x2F3136)
                    embed.set_image(url="attachment://jail.png")

                    embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
                    await message.edit(content="Image processed!", embed=embed)

    @commands.command(description="Gives the member you mentioned a license to be horny", aliases=['waste'])
    async def wasted(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/wasted?avatar={member.avatar.with_format("png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "wasted.png")
                    embed = discord.Embed(title=f"<a:loading:747680523459231834> Processing image...", timestamp=discord.utils.utcnow(), color=0x2F3136)
                    embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
                    message = await ctx.reply(embed=embed, file=file)
                    embed = discord.Embed(title=f"WASTED.", timestamp=discord.utils.utcnow(), color=0x2F3136)
                    embed.set_image(url="attachment://wasted.png")

                    embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
                    await message.edit(content="Image processed!", embed=embed)

    @commands.command(description="Gives the member you mentioned a license to be horny", aliases=['pride', 'gay'])
    async def rainbow(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar.with_format("png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "gay.png")
                    embed = discord.Embed(title=f"<a:loading:747680523459231834> Processing image...", timestamp=discord.utils.utcnow(), color=0x2F3136)
                    embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
                    message = await ctx.reply(embed=embed, file=file)
                    embed = discord.Embed(title=f"{member.name} is now gay", timestamp=discord.utils.utcnow(), color=0x2F3136)
                    embed.set_image(url="attachment://gay.png")

                    embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
                    await message.edit(content="Image processed!", embed=embed)

    @commands.command(description="Gives the member you mentioned a license to be horny")
    async def glass(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/glass?avatar={member.avatar.with_format("png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "glass.png")
                    embed = discord.Embed(title=f"<a:loading:747680523459231834> Processing image...", timestamp=discord.utils.utcnow(), color=0x2F3136)
                    embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
                    message = await ctx.reply(embed=embed, file=file)
                    embed = discord.Embed(title=f"{member.name} is now **glass**", timestamp=discord.utils.utcnow(), color=0x2F3136)
                    embed.set_image(url="attachment://glass.png")

                    embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
                    await message.edit(content="Image processed!", embed=embed)

    @commands.command(alises=['bottoken', 'random_token', 'random_bot_token'], description="Sends a random token of a discord bot")
    async def token(self, ctx):
        embed = discord.Embed(title=f"<a:loading:747680523459231834> Getting token...", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
        message = await ctx.reply(embed=embed)

        async with aiohttp.ClientSession() as session:
            request1 = await session.get('https://some-random-api.ml/bottoken')
            tokenjson = await request1.json()
        embed = discord.Embed(title="Random Bot Token", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.add_field(name="Token", value=f"{tokenjson['token']}")

        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
        await message.edit(content="Received token!", embed=embed)

    @commands.command(description="Shows the size of someones pp!", aliases=['banana', 'eggplant', 'egg_plant'])
    async def pp(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author

        length = random.randint(10, 25)

        embed = discord.Embed(title=f"PP Size - {member}", description=f"8{'=' * length}D\n{member}'s pp is {length} cm", timestamp=discord.utils.utcnow(), color=0x2F3136)

        embed.set_footer(icon_url=ctx.author.avatar.url, text='​')
        await ctx.reply(embed=embed)

    @commands.command(aliases=['8ball', 'magicball', 'magic_ball', 'eight_ball'], description="Answers with yes or no to your question")
    async def eightball(self, ctx, *, question):
        responses = ['It is certain.',
                    'It is decidedly so.',
                    'Without a doubt.',
                    'Yes – definitely.',
                    'You may rely on it.',
                    'As I see it, yes.',
                    'Most likely.',
                    'Outlook good.',
                    'Yes.',
                    'Signs point to yes.',
                    'Reply hazy, try again.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    'Dont count on it.',
                    'My reply is no.',
                    'My sources say no',
                    'Outlook not so good.',
                    'Very doubtful.']

        embed = discord.Embed(title=f"8ball", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.add_field(name="Question: ", value=question, inline=True)
        embed.add_field(name="Answer:",value=random.choice(responses), inline=True)
        await ctx.reply(embed=embed)

    @commands.command(description="Tells you if someone is a furry or not! (This command is a joke)")
    async def furrydetector(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author

        responses = ['Yes',
                    'No']

        embed = discord.Embed(title=f"Furry detector", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.add_field(name="Name", value=f"{member}", inline=True)
        embed.add_field(name="Furry?", value=f"{random.choice(responses)}", inline=True)
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.reply(embed=embed)

    @commands.command(description="Tells you how gay someone is! (This command is a joke)")
    async def gayrate(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author

        embed = discord.Embed(title=f"Gay rate detector", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.add_field(name="Name", value=f"{member}", inline=True)
        embed.add_field(name="Gay rate", value=f"{random.randint(0, 100)}", inline=True)
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.reply(embed=embed)

    @commands.command(description="Tells you a random thing you can do in Minecraft!")
    async def minecraft(self, ctx):
        responses = ['Mine a whole chunk.',
                    'Kill the Wither.',
                    'Get 64 wood logs with a wooden hoe.',
                    'Craft a Netherite Hoe.',
                    'Destroy bedrock (it is possible with glitches)',
                    'Make a Iron Golem farm.',
                    'Throw all your stuff into a chest and start everything from over again.',
                    'Go to End and jump off.',
                    'Swim in lava with Fire Resistance.',
                    'Build a house under the lava in the nether.',
                    'Make a XP farm']

        embed = discord.Embed(title=f"Here's what you should do in minecraft", description=f"{random.choice(responses)}", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.reply(embed=embed)

    @commands.command(help="Generates a random number", aliases=['rm'])
    async def randomnumber(self, ctx, minimum : int=None, maximum : int=None):
        if minimum == None:
            minimum = 1

        if maximum == None:
            maximum = 10

        if maximum > 1000000:
            return await ctx.reply("Number cannot be more than `1000000`.")

        number = random.randint(minimum, maximum)

        await ctx.reply(f"Randomly generated number between `{minimum}` and `{maximum}`: `{number}`")

    @commands.command(help="Generates a random word", aliases=['rw'])
    async def randomword(self, ctx):
        with open("./data/verifyWords.txt", "r") as file:
            allText = file.read()
            wordsList = list(map(str, allText.split()))

        randomWord = random.choice(wordsList)

        await ctx.reply(f"Randomly generated word: {randomWord}")

    @commands.command(help="Tells you a random game you can play in ROBLOX!")
    async def robloxgame(self, ctx):
        responses = ['Jailbreak.',
                    'Flee The Facility.',
                    'Bee Swarm Simulator.',
                    'Mad City.',
                    'Prison Life.',
                    'Doomspire Brickbattle.',
                    'Tapping Simulator.',
                    'Super Power Fighting Simulator.',
                    'Hide n Seek Extreme.',
                    'Anime Fighting Simulator.',
                    'Arsenal.',
                    'Think and ask again.',
                    'Murder Mystery 2.',
                    'Tower Of Hell.',
                    'Islands (Skyblock)',
                    'Bubble Gum Simulator.',
                    'Piggy.',
                    'MeepCity.',
                    'Phantom Forces.',
                    'Brookhaven RP.',
                    'A Bizarre Day.',
                    'Ragdoll Engine.',
                    'Build A Boat For A Treasure.',
                    'Dungeon Quest.',
                    'BIG Paintball.'
                    'The Wild West.',
                    'Car Crushers 2.',
                    'Tower Defense Simulator.',
                    'Work at a Pizza Place.',
                    'Ninja Legends.',
                    'Natural Disasters Survival.',
                    'Zombie Attack.',
                    'RoCitizens.',
                    'Restaurant Tycoon 2.',
                    'Mining Simulator.',
                    'Lifting Simulator.',
                    'Da Hood.',
                    'Counter Blox.',
                    'Kohls Admin House NBC.',
                    'Kohls Admin House BC.',
                    'Epic Minigames.',
                    'Strucid.',
                    'Ro-Ghoul.',
                    'My Restaurant.']

        embed = discord.Embed(title=f"Here's what game you should play in ROBLOX", description=f"{random.choice(responses)}", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.add_field(name="Game name", value=f"{random.choice(responses)}", inline=True)

        await ctx.reply(embed=embed)

    @commands.command(help="Sends a random meme from the r/meme subreddit", aliases=['m'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def meme(self, ctx):
        embed = discord.Embed(title="<a:loading:747680523459231834> Getting meme...", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        message = await ctx.reply(embed=embed)

        sebreddit_list = ["dankmemes", "memes"]
        subreddit = random.choice(sebreddit_list)

        async with self.client.session.get(f"https://www.reddit.com/r/{subreddit}/hot.json") as r:
            response = await r.json()
            redditDict = dict(random.choice(response['data']['children']))
            redditDict = redditDict['data']

            embed = discord.Embed(title=f"{redditDict['title'].upper()}", url=f"https://reddit.com{redditDict['permalink']}", description=f"<:upvote:274492025678856192> Upvotes: {redditDict['ups']}\nComments: {redditDict['num_comments']}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_image(url=redditDict['url'])
            embed.set_footer(text=f"Command requested by: {ctx.author} • Subreddit: {subreddit}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

    @commands.command(help="Shows you a random meme from the subreddit r/ProgrammerHumor", aliases=['programmer_meme', 'programmeme', 'program_meme', 'pm'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def programmermeme(self, ctx):
        embed = discord.Embed(title="<a:loading:747680523459231834> Getting programmer meme...", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        message = await ctx.reply(embed=embed)

        sebreddit_list = ["ProgrammerHumor", "ProgrammerHumor"]
        subreddit = random.choice(sebreddit_list)

        async with self.client.session.get(f"https://www.reddit.com/r/{subreddit}/hot.json") as r:
            response = await r.json()
            redditDict = dict(random.choice(response['data']['children']))
            redditDict = redditDict['data']

            embed = discord.Embed(title=f"{redditDict['title'].upper()}", url=f"https://reddit.com{redditDict['permalink']}", description=f"<:upvote:274492025678856192> Upvotes: {redditDict['ups']}\nComments: {redditDict['num_comments']}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_image(url=redditDict['url'])
            embed.set_footer(text=f"Command requested by: {ctx.author} • Subreddit: {subreddit}", icon_url=ctx.author.avatar.url)

            await message.edit(embed=embed)

    @commands.command(description="Messages you.", aliases=['msg_me'])
    async def msgme(self, ctx, *, content):
        try:
            await ctx.author.send(content)
            await ctx.reply("Successfully messaged you.")
        except:
            await ctx.reply("I couldn't message you, make sure your private messages are enabled.")

    @commands.command(description="Let's you hug someone!")
    async def hug(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author
            async with aiohttp.ClientSession() as session:
                request = await session.get('https://some-random-api.ml/animu/hug')
                hugjson = await request.json()

            embed = discord.Embed(title=f"{ctx.author} hugged {member}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_image(url=hugjson['link'])
            embed.set_footer(text=f"Command requested by: {ctx.author}"	, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
            return

    @commands.command(description="Let's you pat someone!")
    async def pat(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author
            async with aiohttp.ClientSession() as session:
                request = await session.get('https://some-random-api.ml/animu/pat')
                patjson = await request.json()

            embed = discord.Embed(title=f"{ctx.author} patted {member}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_image(url=patjson['link'])
            embed.set_footer(text=f"Command requested by: {ctx.author}"	, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
            return

    @commands.command(description="Let's you wink at someone!")
    async def wink(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author
            async with aiohttp.ClientSession() as session:
                request = await session.get('https://some-random-api.ml/animu/wink')
                winkjson = await request.json()

            embed = discord.Embed(title=f"{ctx.author} winked at {member}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_image(url=winkjson['link'])
            embed.set_footer(text=f"Command requested by: {ctx.author}"	, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
            return

    @commands.command(description="Let's you reverse some text")
    async def reverse(self, ctx, *, text):
        embed = discord.Embed(title=f"Text reversed", description=f"""
Original text: {text}
<:reverse:879724816834375791> Reveresd text: {text[::-1]}
        """, timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_footer(text=f"Command requested by: {ctx.author}"	, icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    @commands.command(help="OOF's the person you mentioned", aliases=['commitoof', 'commit_oof'])
    async def oof(self, ctx, member : discord.Member=None):
        if member == None or member == ctx.author:
            responses = [f"{ctx.author.name} was killed in Electrical.",
            f"{ctx.author.name} failed math.",
            f"{ctx.author.name} rolled down a large hill.",
            f"{ctx.author.name} cried to death.",
            f"{ctx.author.name} smelt their own socks.",
            f"{ctx.author.name} forgot to stop texting while driving. Don't text and drive, kids.",
            f"{ctx.author.name} said Among Us in a public chat.",
            f"{ctx.author.name} stubbed their toe.",
            f"{ctx.author.name} forgot to grippen their shoes when walking down the stairs.",
            f"{ctx.author.name} wasn't paying attention and stepped on a mine.",
            f"{ctx.author.name} held a grenade for too long.",
            f"{ctx.author.name} got pwned by a sweaty tryhard.",
            f"{ctx.author.name} wore a black shirt in the summer.",
            f"{ctx.author.name} burned to a crisp.",
            f"{ctx.author.name} choked on a chicken nugget.",
            f"{ctx.author.name} forgot to look at the expiration date on the food.",
            f"{ctx.author.name} ran into a wall.",
            f"{ctx.author.name} shook a vending machine too hard.",
            f"{ctx.author.name} was struck by lightning.",
            f"{ctx.author.name} chewed 5 gum.",
            f"{ctx.author.name} ate too many vitamin gummy bears.",
            f"{ctx.author.name} tried to swim in lava. Why would you ever try to do that?"]
            return await ctx.reply(f"{random.choice(responses)}")
        else:
            responses = [f"{ctx.author.name} exploded {member.name}.",
                        f"{ctx.author.name} shot {member.name}.",
                        f"{ctx.author.name} went ham on {member.name}.",
                        f"{ctx.author.name} betrayed and killed {member.name}.",
                        f"{ctx.author.name} sent {member.name} to Davy Jones' locker.",
                        f"{ctx.author.name} no scoped {member.name}.",
                        f"{ctx.author.name} said no u and killed {member.name}.",
                        f"{ctx.author.name} blew up {member.name} with a rocket.",
                        f"{ctx.author.name} pushed {member.name} off a cliff.",
                        f"{ctx.author.name} stabbed {member.name} to death.",
                        f"{ctx.author.name} slammed {member.name} with a chair.",
                        f"{ctx.author.name} recited a magic spell and killed {member.name}.",
                        f"{ctx.author.name} electrified {member.name}.",
                        f"{member.name} was slain by {ctx.author.name}.",
                        f"{ctx.author.name} burnt {member.name} alive.",
                        f"{ctx.author.name} buried {member.name}.",
                        f"{ctx.author.name} shoved {member.name}'s head underwater for too long.",
                        f"{ctx.author.name} slid a banana peel under {member.name}'s feet. They tripped and died...",
                        f"{ctx.author.name} got a headshot on {member.name}.",
                        f"{ctx.author.name} said a hilarious joke to {member.name} and died.",
                        f"{ctx.author.name} showed old Vicente0670 videos to {member.name} and died of cringe.",
                        f"{ctx.author.name} didn't buy Panda Express for {member.name} and exploded.",
                        f"{ctx.author.name} sent {member.name} to the Nether.",
                        f"{ctx.author.name} tossed {member.name} off an airplane.",
                        f"{ctx.author.name} broke {member.name}'s neck."]

            await ctx.reply(f"{random.choice(responses)}")

    # @commands.command(help="Let's you commit suicide", aliases=['suicied', 'suiced'])
    # async def suicide(self, ctx):
    #     responses = [f"{ctx.author.name} said, goodbye cruel world!",
    #                 f"{ctx.author.name} commited sudoku.",
    #                 f"{ctx.author.name} tripped down a mountain.",
    #                 f"{ctx.author.name} stabbed themselves.",
    #                 f"{ctx.author.name} smelt their socks.",
    #                 f"{ctx.author.name} banged their head with a pan.",
    #                 f"{ctx.author.name} held the knife the wrong way.",
    #                 f"{ctx.author.name} stubbed their toe.",
    #                 f"{ctx.author.name} forgot to grippen their shoes when walking down the stairs.",
    #                 f"{ctx.author.name} stepped on a mine.",
    #                 f"{ctx.author.name} held a grenade for too long.",
    #                 f"{ctx.author.name} jumped off a cliff.",
    #                 f"{ctx.author.name} wore a black shirt in the summer.",
    #                 f"{ctx.author.name} caught on fire.",
    #                 f"{ctx.author.name} choked on a chicken nugget.",
    #                 f"{ctx.author.name} ate expired Oreos.",
    #                 f"{ctx.author.name} hit their head on the wall.",
    #                 f"{ctx.author.name} shook a vending machine too hard.",
    #                 f"{ctx.author.name} was struck by lightning.",
    #                 f"{ctx.author.name} chewed 5 gum.",
    #                 f"{ctx.author.name} ate too many vitamin gummy bear.",
    #                 f"{ctx.author.name} tried to swim in lava. Why would you ever try to do that?"]
    #
    #     await ctx.reply(f"{random.choice(responses)}")


def setup(client):
    client.add_cog(fun(client))
