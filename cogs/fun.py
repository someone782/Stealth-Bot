from aiohttp import helpers
import discord
import random
import helpers
import asyncio
import io
import datetime
import aiohttp
import pyfiglet
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

def setup(client):
    client.add_cog(fun(client))

class fun(commands.Cog):
    "🤪 Fun commands like -meme, -hug and more"
    def __init__(self, client):
        self.client = client

    @commands.command(help="Turns any text into ASCII", aliases=['asciitext', 'ascii_text', 'gen_ascii', 'generator_ascii'])
    async def ascii(self, ctx, *, text):
        if len(text) > 10:
            return await ctx.send("Your ASCII text exceeded the 10-character limit.")
        
        ascii = pyfiglet.figlet_format(text)

        embed = discord.Embed(title="ASCII", description=f"""
Original text: {text}
ASCII Text:
```
{ascii}
```
                              """)

        await ctx.send(embed=embed)

    @commands.command(help="Sends a image of the member you mention but triggered")
    @commands.cooldown(1, 5, BucketType.member)
    async def triggered(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar.with_format("png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "triggered.gif")
                    embed = discord.Embed(title=f"<a:loading:747680523459231834> Processing image...")
                    
                    message = await ctx.send(embed=embed, file=file)
                    embed = discord.Embed(title=f"{member.name} is triggered")
                    embed.set_image(url="attachment://triggered.gif")

                    await message.edit(content="Image processed!", embed=embed)

    @commands.command(help="Gives the member you mentioned a license to be horny", aliases=['horny_license', 'license_horny'])
    @commands.cooldown(1, 5, BucketType.member)
    async def horny(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/horny?avatar={member.avatar.with_format("png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")
                    embed = discord.Embed(title=f"<a:loading:747680523459231834> Processing image...")
                    
                    message = await ctx.send(embed=embed, file=file)
                    embed = discord.Embed(title=f"{member.name} has the license to be horny")
                    embed.set_image(url="attachment://horny.png")

                    await message.edit(content="Image processed!", embed=embed)

    @commands.command(help="Gives the member you mentioned a license to be horny", aliases=['go_to_jail', 'in_jail'])
    @commands.cooldown(1, 5, BucketType.member)
    async def jail(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/jail?avatar={member.avatar.with_format("png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "jail.png")
                    embed = discord.Embed(title=f"<a:loading:747680523459231834> Processing image...")
                    
                    message = await ctx.send(embed=embed, file=file)
                    embed = discord.Embed(title=f"{member.name} has been sent to jail for 69420 years")
                    embed.set_image(url="attachment://jail.png")

                    await message.edit(content="Image processed!", embed=embed)

    @commands.command(help="Gives the member you mentioned a license to be horny", aliases=['waste'])
    @commands.cooldown(1, 5, BucketType.member)
    async def wasted(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/wasted?avatar={member.avatar.with_format("png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "wasted.png")
                    embed = discord.Embed(title=f"<a:loading:747680523459231834> Processing image...")
                    
                    message = await ctx.send(embed=embed, file=file)
                    embed = discord.Embed(title=f"WASTED.")
                    embed.set_image(url="attachment://wasted.png")

                    await message.edit(content="Image processed!", embed=embed)

    @commands.command(help="Gives the member you mentioned a license to be horny", aliases=['pride', 'gay'])
    @commands.cooldown(1, 5, BucketType.member)
    async def rainbow(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar.with_format("png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "gay.png")
                    embed = discord.Embed(title=f"<a:loading:747680523459231834> Processing image...")
                    
                    message = await ctx.send(embed=embed, file=file)
                    embed = discord.Embed(title=f"{member.name} is now gay")
                    embed.set_image(url="attachment://gay.png")


                    await message.edit(content="Image processed!", embed=embed)

    @commands.command(help="Gives the member you mentioned a license to be horny")
    @commands.cooldown(1, 5, BucketType.member)
    async def glass(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/glass?avatar={member.avatar.with_format("png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "glass.png")
                    embed = discord.Embed(title=f"<a:loading:747680523459231834> Processing image...")
                    
                    message = await ctx.send(embed=embed, file=file)
                    embed = discord.Embed(title=f"{member.name} is now **glass**")
                    embed.set_image(url="attachment://glass.png")
                    
                    await message.edit(content="Image processed!", embed=embed)

    @commands.command(help="Sends a random token of a discord bot", alises=['bottoken', 'random_token', 'random_bot_token'])
    @commands.cooldown(1, 5, BucketType.member)
    async def token(self, ctx):
        embed = discord.Embed(title=f"<a:loading:747680523459231834> Getting token...")
        
        message = await ctx.send(embed=embed)

        async with aiohttp.ClientSession() as session:
            request1 = await session.get('https://some-random-api.ml/bottoken')
            tokenjson = await request1.json()
        embed = discord.Embed(title="Random Bot Token", description=f"""
Token: {tokenjson['token']}
                              """)
        
        await message.edit(content="Received token!", embed=embed)

    @commands.command(help="Shows the size of someones pp!", aliases=['banana', 'eggplant', 'egg_plant'])
    async def pp(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author

        length = random.randint(10, 25)

        embed = discord.Embed(title=f"PP Size - {member}", description=f"8{'=' * length}D\n{member.name}'s :eggplant: is {length} cm")

        await ctx.send(embed=embed)

    @commands.command(help="Answers with yes or no to your question", aliases=['8ball', 'magicball', 'magic_ball', 'eight_ball'])
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
                    'send hazy, try again.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    'Dont count on it.',
                    'My send is no.',
                    'My sources say no',
                    'Outlook not so good.',
                    'Very doubtful.']

        embed = discord.Embed(title=f"8ball", description=f"""
Question: {question}
Answer: {random.choice(responses)}
                              """)
        
        await ctx.send(embed=embed)

    @commands.command(help="Tells you if someone is a furry or not")
    async def furrydetector(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author

        responses = ['is a furry.',
                    'is not a furry.']
        
        await ctx.send(f"{member} {random.choice(responses)}")

    @commands.command(help="Tells you how gay someone is")
    async def gayrate(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author

        await ctx.send(f"{member} is {random.randint(0, 100)}% gay!")

    @commands.command(help="Generates a random number", aliases=['rm'])
    async def randomnumber(self, ctx, minimum : int=None, maximum : int=None):
        if minimum == None:
            minimum = 1

        if maximum == None:
            maximum = 10

        if maximum > 1000000:
            return await ctx.send("Number cannot be more than `1000000`.")

        number = random.randint(minimum, maximum)

        await ctx.send(f"Randomly generated number between `{minimum}` and `{maximum}`: `{number}`")

    @commands.command(help="Generates a random word", aliases=['rw'])
    async def randomword(self, ctx):
        with open("./data/verifyWords.txt", "r") as file:
            allText = file.read()
            wordsList = list(map(str, allText.split()))

        randomWord = random.choice(wordsList)

        await ctx.send(f"Here's a randomly generated word: `{randomWord}`")

    @commands.command(help="Sends a random meme from the r/meme subreddit", aliases=['m'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def meme(self, ctx):
        embed = discord.Embed(title="<a:loading:747680523459231834> Getting meme...")
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        message = await ctx.send(embed=embed)

        sebreddit_list = ["dankmemes", "memes"]
        subreddit = random.choice(sebreddit_list)

        async with self.client.session.get(f"https://www.reddit.com/r/{subreddit}/hot.json") as r:
            response = await r.json()
            redditDict = dict(random.choice(response['data']['children']))
            redditDict = redditDict['data']

            embed = discord.Embed(title=f"{redditDict['title'].upper()}", url=f"https://reddit.com{redditDict['permalink']}", description=f"<:upvote:274492025678856192> Upvotes: {redditDict['ups']}\nComments: {redditDict['num_comments']}")
            embed.set_image(url=redditDict['url'])

            await message.edit(embed=embed)

    @commands.command(help="Shows you a random meme from the subreddit r/ProgrammerHumor", aliases=['programmer_meme', 'programmeme', 'program_meme', 'pm'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def programmermeme(self, ctx):
        embed = discord.Embed(title="<a:loading:747680523459231834> Getting programmer meme...")
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        message = await ctx.send(embed=embed)

        sebreddit_list = ["ProgrammerHumor", "ProgrammerHumor"]
        subreddit = random.choice(sebreddit_list)

        async with self.client.session.get(f"https://www.reddit.com/r/{subreddit}/hot.json") as r:
            response = await r.json()
            redditDict = dict(random.choice(response['data']['children']))
            redditDict = redditDict['data']

            embed = discord.Embed(title=f"{redditDict['title'].upper()}", url=f"https://reddit.com{redditDict['permalink']}", description=f"<:upvote:274492025678856192> Upvotes: {redditDict['ups']}\nComments: {redditDict['num_comments']}")
            embed.set_image(url=redditDict['url'])

            await message.edit(embed=embed)

    @commands.command(help="Shows you a random piece of art from the subreddit r/Art", aliases=['drawing', 'arts', 'artist'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def art(self, ctx):
        embed = discord.Embed(title="<a:loading:747680523459231834> Getting piece of art...")
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        message = await ctx.send(embed=embed)

        sebreddit_list = ["Art", "ArtBattle"]
        subreddit = random.choice(sebreddit_list)

        async with self.client.session.get(f"https://www.reddit.com/r/{subreddit}/hot.json") as r:
            response = await r.json()
            redditDict = dict(random.choice(response['data']['children']))
            redditDict = redditDict['data']

            embed = discord.Embed(title=f"{redditDict['title'].upper()}", url=f"https://reddit.com{redditDict['permalink']}", description=f"<:upvote:274492025678856192> Upvotes: {redditDict['ups']}\nComments: {redditDict['num_comments']}")
            embed.set_image(url=redditDict['url'])

            await message.edit(embed=embed)

    @commands.command(help="Messages you.", aliases=['msg_me'])
    async def msgme(self, ctx, *, content):
        try:
            await ctx.author.send(content)
            await ctx.send("Successfully messaged you.")
            
        except:
            await ctx.send("I couldn't message you, make sure your private messages are enabled.")

    @commands.command(help="Let's you hug someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def hug(self, ctx, member : discord.Member):
        if member == None:
            return await ctx.send("You can't hug yourself!")
            
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/animu/hug')
            hugjson = await request.json()

        embed = discord.Embed(title=f"{ctx.author} hugged {member}")
        embed.set_image(url=hugjson['link'])
        
        await ctx.send(embed=embed)

    @commands.command(description="Let's you pat someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def pat(self, ctx, member : discord.Member=None):
        if member == None:
            return await ctx.send("You can't pat yourself!")
        
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/animu/pat')
            patjson = await request.json()

        embed = discord.Embed(title=f"{ctx.author} patted {member}")
        embed.set_image(url=patjson['link'])
        
        await ctx.send(embed=embed)

    @commands.command(description="Let's you wink at someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def wink(self, ctx, member : discord.Member=None):
        if member == None:
            return await ctx.send("You can't wink at yourself!")
            
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/animu/wink')
            winkjson = await request.json()

        embed = discord.Embed(title=f"{ctx.author} winked at {member}")
        embed.set_image(url=winkjson['link'])
        
        await ctx.send(embed=embed)

    @commands.command(description="Let's you reverse some text")
    async def reverse(self, ctx, *, text):
        embed = discord.Embed(title=f"Text reversed", description=f"""
Original text: {text}
<:reverse:879724816834375791> Reveresd text: {text[::-1]}
        """)
        
        await ctx.send(embed=embed)

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
            return await ctx.send(f"{random.choice(responses)}")
        
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

            await ctx.send(f"{random.choice(responses)}")


    # this command was removed due to top.gg not accepting my bot cause it "promotes suicide"

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
    #     await ctx.send(f"{random.choice(responses)}")
