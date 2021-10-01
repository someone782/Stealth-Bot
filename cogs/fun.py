from aiohttp import helpers
import discord
import random
import helpers.helpers as helpers
import asyncio
import re
import io
import datetime
import aiohttp
import time
import pyfiglet
from discord.ext import commands, menus
from discord.ext.menus.views import ViewMenuPages
from discord.ext.commands.cooldowns import BucketType

def setup(client):
    client.add_cog(Fun(client))

class Fun(commands.Cog):
    ":soccer: | Fun commands like meme, hug and more" 
    def __init__(self, client):
        self.client = client
        
    async def reddit(self, subreddit: str, title: bool = False, embed_type: str = 'IMAGE') -> discord.Embed:
        subreddit = await self.client.reddit.subreddit(subreddit)
        post = await subreddit.random()

        if embed_type == 'IMAGE':
            while 'i.redd.it' not in post.url or post.over_18:
                post = await subreddit.random()

            embed = discord.Embed(description=f"🌐 [Post](https://reddit.com{post.permalink}) • "
                                              f"<:upvote:274492025678856192> {post.score} ({post.upvote_ratio * 100}%) "
                                              f"• from [r/{subreddit}](https://reddit.com/r/{subreddit})")
            embed.title = post.title if title is True else None
            embed.set_image(url=post.url)
            return embed

        if embed_type == 'POLL':
            while not hasattr(post, 'poll_data') or not post.poll_data or post.over_18:
                post = await (await self.client.reddit.subreddit(subreddit)).random()

            iterations: int = 1
            options = []
            emojis = []
            for option in post.poll_data.options:
                num = f"{iterations}\U0000fe0f\U000020e3"
                options.append(f"{num} {option.text}")
                emojis.append(num)
                iterations += 1
                if iterations > 9:
                    iterations = 1

            embed = discord.Embed(color=discord.Color.random(),
                                  description='\n'.join(options))
            embed.title = post.title if title is True else None
            return embed, emojis
        
    @commands.command()
    async def meme2(self, ctx):
        """
        Sends a random meme from reddit.com/r/memes.
        """
        async with ctx.typing():
            return await ctx.send(embed=await self.reddit(random.choice(['memes', 'dankmemes'])))
        
    @commands.command(
        help="Ships you with someone")
    async def ship(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                
        number1 = random.randint(0, 100)
        
        number2 = int(str(number1)[:-1] + '0')
        
        if number2 == 10:
            text = "<:notlikethis:596577155169910784> Yikes.. That's bad."
        elif number2 == 20:
            text = "<:blobsweatsip:759934644807401512> Maybe?.. I doubt thought."
        elif number2 == 30:
            text = "<:blobpain:739614945045643447> Hey it's not terrible.. It could be worse."
        elif number2 == 40:
            text = "<:monkaS:596577132063490060> Not bad!"
        elif number2 == 50:
            text = "<:flooshed:814095751042039828> Damn!"
        elif number2 == 60:
            text = "<:pogu2:787676797184770060> AYOOO POG"
        elif number2 == 70:
            text = "<:rooAww:747680003021471825> That has to be a ship!"
        elif number2 == 80:
            text = "<a:rooClap:759933903959228446> That's a ship!"
        elif number2 == 90:
            text = ":flushed: Wow!"
        elif number2 == 100:
            text = "<:drakeYea:596577437182197791> That's a ship 100%"
        else:
            text = "<:thrinking:597590667669274651> I don't know man.."
            
        await ctx.send(f"{text}\n{ctx.author.name} & {member.name}\n{number1}%")
        
    @commands.command(
        help="Rick rolls someone")
    async def rickroll(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                
        text = f"""
Never gonna give {member.mention} up
Never gonna let {member.mention} down
Never gonna run around and desert {member.mention}
Never gonna make {member.mention} cry
Never gonna say goodbye
Never gonna tell a lie and hurt {member.mention}
Never gonna give {member.mention} up
Never gonna let {member.mention} down
Never gonna run around and desert {member.mention}
Never gonna make {member.mention} cry
Never gonna say goodbye
Never gonna tell a lie and hurt {member.mention}
Never gonna give {member.mention} up
Never gonna let {member.mention} down
Never gonna run around and desert {member.mention}
Never gonna make {member.mention} cry
Never gonna say goodbye
Never gonna tell a lie and hurt {member.mention}
        """
        
        await ctx.send(text, reply=False)

    @commands.command(
        help="Turns any text into ASCII",
        aliases=['asciitext', 'ascii_text', 'gen_ascii', 'generator_ascii'])
    async def ascii(self, ctx, *, text):
        if len(text) > 20:
            return await ctx.send("Your ASCII text exceeded the 20-character limit.")
        
        ascii = pyfiglet.figlet_format(text)

        embed = discord.Embed(title="ASCII",
                              description=f"""
```
{ascii}
```
                              """)

        await ctx.send(embed=embed)

    @commands.command(
        help="Sends a image of the member you mention but triggered")
    @commands.cooldown(1, 5, BucketType.member)
    async def triggered(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author


        af = await self.client.session.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar.with_format("png")}')
        if 300 > af.status >= 200:
                fp = io.BytesIO(await af.read())
                file = discord.File(fp, "triggered.gif")
                    
                embed = discord.Embed(title=f"{member.name} is triggered")
                embed.set_image(url="attachment://triggered.gif")

                await ctx.send(embed=embed, file=file)

    @commands.command(
        help="Gives the member you mentioned a license to be horny",
        aliases=['horny_license', 'license_horny'])
    @commands.cooldown(1, 5, BucketType.member)
    async def horny(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author

        af = await self.client.session.get(f'https://some-random-api.ml/canvas/horny?avatar={member.avatar.with_format("png")}')
        if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")

                    embed = discord.Embed(title=f"{member.name} has the license to be horny")
                    embed.set_image(url="attachment://horny.png")

                    await ctx.send(embed=embed, file=file)

    @commands.command(
        help="Gives the member you mentioned a license to be horny",
        aliases=['go_to_jail', 'in_jail'])
    @commands.cooldown(1, 5, BucketType.member)
    async def jail(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author

            af = await self.client.session.get(f'https://some-random-api.ml/canvas/jail?avatar={member.avatar.with_format("png")}')
            if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "jail.png")

                    embed = discord.Embed(title=f"{member.name} has been sent to jail for 69420 years")
                    embed.set_image(url="attachment://jail.png")

                    await ctx.send(embed=embed, file=file)

    @commands.command(
        help="Gives the member you mentioned a license to be horny",
        aliases=['waste'])
    @commands.cooldown(1, 5, BucketType.member)
    async def wasted(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author

        af = await self.client.session.get(f'https://some-random-api.ml/canvas/wasted?avatar={member.avatar.with_format("png")}')
        if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "wasted.png")

                    embed = discord.Embed(title=f"WASTED.")
                    embed.set_image(url="attachment://wasted.png")

                    await ctx.send(embed=embed, file=file)

    @commands.command(
        help="Gives the member you mentioned a license to be horny",
        aliases=['pride', 'gay'])
    @commands.cooldown(1, 5, BucketType.member)
    async def rainbow(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author

        af = await self.client.session.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar.with_format("png")}')
        if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "gay.png")

                    embed = discord.Embed(title=f"{member.name} is now gay")
                    embed.set_image(url="attachment://gay.png")

                    await ctx.send(embed=embed, file=file)

    @commands.command(
        help="Puts you behind glass")
    @commands.cooldown(1, 5, BucketType.member)
    async def glass(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author

        af = await self.client.session.get(f'https://some-random-api.ml/canvas/glass?avatar={member.avatar.with_format("png")}')
        if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "glass.png")

                    embed = discord.Embed(title=f"{member.name} is now **glass**")
                    embed.set_image(url="attachment://glass.png")
                    
                    await ctx.send(embed=embed, file=file)

    @commands.command(
        help="Sends a random token of a discord bot",
        alises=['bottoken', 'random_token', 'random_bot_token'])
    @commands.cooldown(1, 5, BucketType.member)
    async def token(self, ctx):
        request1 = await self.client.session.get('https://some-random-api.ml/bottoken')
        tokenjson = await request1.json()
        embed = discord.Embed(title="Random Bot Token", description=f"{tokenjson['token']}")
        
        await ctx.send(embed=embed)

    @commands.command(
        help="Shows the size of someones pp!",
        aliases=['banana', 'eggplant', 'egg_plant'])
    async def pp(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author

        length = random.randint(10, 25)

        embed = discord.Embed(title=f"PP Size - {member}",
                              description=f"8{'=' * length}D\n{member.name}'s :eggplant: is {length} cm")

        await ctx.send(embed=embed)

    @commands.command(
        help="Answers with yes or no to your question",
        aliases=['8ball', 'magicball', 'magic_ball', 'eight_ball'])
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
                    'Don\'t count on it.',
                    'My reply is no.',
                    'My sources say no',
                    'Outlook not so good.',
                    'Very doubtful.']

        embed = discord.Embed(title=f"8ball", description=f"""
Question: {question}
Answer: {random.choice(responses)}
                              """)
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Answers with yes or no",
        aliases=['yes', 'no', 'yes_no', 'yesorno', 'yes_or_no'])
    async def yesno(self, ctx):
        start = time.perf_counter()
        
        request1 = await self.client.session.get('https://yesno.wtf/api')
        json = await request1.json()
        
        end = time.perf_counter()
        
        ms = (end - start) * 1000
        
        embed = discord.Embed(title=f"{json['answer']}")
        embed.set_image(url=json['image'])
        embed.set_footer(text=f"{round(ms)}ms{' ' * (9-len(str(round(ms, 3))))}", icon_url=ctx.author.avatar.url)
        
        await ctx.send(embed=embed)

    @commands.command(
        help="Chooses between multiple choices.\nTo denote multiple choices, you should use double quotes.",
        aliases=['choice', 'decide'])
    async def choose(self, ctx, *choices : commands.clean_content):
        if len(choices) < 2:
            return await ctx.send("Not enough choices.")

        await ctx.send(f"I choose `{random.choice(choices)}`.")
        
    @commands.command(
        help="Replaces all spaces in given text with a clapping emoji",
        aliases=['applause'])
    async def clap(self, ctx, *, text : str):
        text = text.replace(" ", " 👏 ")
        
        if len(text) > 1000:
            return await ctx.send("That text is over the 1000-character limit.")
        
        embed = discord.Embed(description=f"{text}")
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Replaces all spaces in given text with a emoji/character",
        aliases=['ins'])
    async def insert(self, ctx, character : str, *, text : str):
        text = text.replace(" ", f" {character} ")
        
        if len(text) > 1000:
            return await ctx.send("That text is over the 1000-character limit.")
        
        embed = discord.Embed(description=f"{text}")
        
        await ctx.send(embed=embed)

    @commands.command(
        help="Tells you if someone is a furry or not")
    async def furrydetector(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author

        responses = ['is a furry.',
                    'is not a furry.']
        
        await ctx.send(f"{member} {random.choice(responses)}")

    @commands.command(
        help="Tells you how gay someone is")
    async def gayrate(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author

        await ctx.send(f"{member} is {random.randint(0, 100)}% gay!")

    @commands.command(
        help="Tells you a random number with a optional range. Minimum has to be smaller than maximum",
        aliases=['random_number', 'randomnumber', 'number_random', 'numberrandom'])
    async def number(self, ctx, minimum : int=0, maximum : int=100):
        maximum = min(maximum, 1000)
        if minimum >= maximum:
            return await ctx.send("The maximum number has to be bigger than the minimum number")

        await ctx.send(f"Randomly generated number between `{minimum}` and `{maximum}`: `{random.randint(minimum, maximum)}`")

    @commands.command(
        help="Generates a random word",
        aliases=['rw'])
    async def randomword(self, ctx):
        with open("./data/verifyWords.txt", "r") as file:
            allText = file.read()
            wordsList = list(map(str, allText.split()))

        randomWord = random.choice(wordsList)

        await ctx.send(f"Here's a randomly generated word: `{randomWord}`")

    @commands.command(
        help="Rolls a random dice",
        aliases=['randomdice', 'random_dice', 'rolladice', 'rolldice', 'roll_a_dice', 'roll_dice'])
    async def dice(self, ctx):
        responses = ['<:dice_1:883581027744907304>',
                    '<:dice_2:883581054626177105> ',
                    '<:dice_3:883581082803511336>',
                    '<:dice_4:883581104026681365>',
                    '<:dice_5:883581129360285726>',
                    '<:dice_6:883581159412490250>']
        
        await ctx.send(f"{random.choice(responses)}")

    @commands.command(
        help="Sends a random meme from the r/meme subreddit",
        aliases=['m'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def meme(self, ctx):
        embed = discord.Embed(title="<a:loading:747680523459231834> Getting meme...")
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        message = await ctx.send(embed=embed)

        sebreddit_list = ["dankmemes", "memes"]
        subreddit = random.choice(sebreddit_list)

        r = await self.client.session.get(f"https://www.reddit.com/r/{subreddit}/hot.json")
        response = await r.json()
        redditDict = dict(random.choice(response['data']['children']))
        redditDict = redditDict['data']

        embed = discord.Embed(title=f"{redditDict['title'].upper()}", url=f"https://reddit.com{redditDict['permalink']}", description=f"<:upvote:274492025678856192> Upvotes: {redditDict['ups']}\nComments: {redditDict['num_comments']}")
        embed.set_image(url=redditDict['url'])

        await message.edit(embed=embed)

    @commands.command(
        help="Shows you a random meme from the subreddit r/ProgrammerHumor",
        aliases=['programmer_meme', 'programmeme', 'program_meme', 'pm'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def programmermeme(self, ctx):
        embed = discord.Embed(title="<a:loading:747680523459231834> Getting programmer meme...")
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        message = await ctx.send(embed=embed)

        sebreddit_list = ["ProgrammerHumor", "ProgrammerHumor"]
        subreddit = random.choice(sebreddit_list)

        r = await self.client.session.get(f"https://www.reddit.com/r/{subreddit}/hot.json")
        response = await r.json()
        redditDict = dict(random.choice(response['data']['children']))
        redditDict = redditDict['data']

        embed = discord.Embed(title=f"{redditDict['title'].upper()}", url=f"https://reddit.com{redditDict['permalink']}", description=f"<:upvote:274492025678856192> Upvotes: {redditDict['ups']}\nComments: {redditDict['num_comments']}")
        embed.set_image(url=redditDict['url'])

        await message.edit(embed=embed)

    @commands.command(
        help="Shows you a random piece of art from the subreddit r/Art",
        aliases=['drawing', 'arts', 'artist'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def art(self, ctx):
        embed = discord.Embed(title="<a:loading:747680523459231834> Getting piece of art...")
        embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

        message = await ctx.send(embed=embed)

        sebreddit_list = ["Art", "ArtBattle"]
        subreddit = random.choice(sebreddit_list)

        r = await self.client.session.get("https://www.reddit.com/r/{subreddit}/hot.json")
        response = await r.json()
        redditDict = dict(random.choice(response['data']['children']))
        redditDict = redditDict['data']

        embed = discord.Embed(title=f"{redditDict['title'].upper()}", url=f"https://reddit.com{redditDict['permalink']}", description=f"<:upvote:274492025678856192> Upvotes: {redditDict['ups']}\nComments: {redditDict['num_comments']}")
        embed.set_image(url=redditDict['url'])

        await message.edit(embed=embed)

    @commands.command(
        help="Messages you.",
        aliases=['msg_me'])
    async def msgme(self, ctx, *, content):
        try:
            await ctx.author.send(content)
            await ctx.send("Successfully messaged you.")
            
        except:
            await ctx.send("I couldn't message you, make sure your private messages are enabled.")

    @commands.command(
        help="Let's you hug someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def hug(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't hug yourself!")
            
        request = await self.client.session.get('https://api.waifu.pics/sfw/hug')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} hugged {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)

    @commands.command(
        help="Let's you pat someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def pat(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't pat yourself!")
            
        request = await self.client.session.get('https://api.waifu.pics/sfw/pat')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} patted {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Let's you kiss someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def kiss(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't kiss yourself!")
            
        request = await self.client.session.get('https://api.waifu.pics/sfw/kiss')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} kissed {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Let's you pat someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def pat(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't pat yourself!")
            
        request = await self.client.session.get('https://api.waifu.pics/sfw/pat')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} patted {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Let's you lick someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def lick(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't lick yourself!")
            
        
        request = await self.client.session.get('https://api.waifu.pics/sfw/lick')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} licked {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Let's you bonk someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def bonk(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't bonk yourself!")
            
        request = await self.client.session.get('https://api.waifu.pics/sfw/bonk')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} bonked {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Let's you bully someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def bully(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't bully yourself!")
            
        request = await self.client.session.get('https://api.waifu.pics/sfw/bully')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} bullied {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Let's you cuddle someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def cuddle(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't cuddle yourself!")
            
        request = await self.client.session.get('https://api.waifu.pics/sfw/cuddle')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} cuddled {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Let's you cuddle someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def cuddle(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't cuddle yourself!")
            
        request = await self.client.session.get('https://api.waifu.pics/sfw/cuddle')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} cuddled {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Let's you slap someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def slap(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't slap yourself!")
            
        request = await self.client.session.get('https://api.waifu.pics/sfw/slap')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} slapped {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Let's you yeet someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def yeet(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't yeet yourself!")

        request = await self.client.session.get('https://api.waifu.pics/sfw/yeet')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} yeeted {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Let's you wave at someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def wave(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't hug yourself!")

        request = await self.client.session.get('https://api.waifu.pics/sfw/wave')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} waved at {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Let's you high five someone!",
        aliases=['high_five'])
    @commands.cooldown(1, 5, BucketType.member)
    async def highfive(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't high five yourself!")

        request = await self.client.session.get('https://api.waifu.pics/sfw/highfive')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} high fived {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)

    @commands.command(
        help="Let's you bite someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def bite(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            else:
                member = ctx.author
                return await ctx.send("You can't bite yourself!")

        request = await self.client.session.get('https://api.waifu.pics/sfw/bite')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} bit {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
    help="Let's you kill someone!")
    @commands.cooldown(1, 5, BucketType.member)
    async def kill(self, ctx, member : discord.Member=None):
        if member is None:
            if ctx.message.reference:
                member = ctx.message.reference.resolved.author
            elif member.id == ctx.author.id:
                return await ctx.send("what u trying do mate")

        request = await self.client.session.get('https://api.waifu.pics/sfw/kill')
        json = await request.json()

        embed = discord.Embed(title=f"{ctx.author.name} killed {member.name}")
        embed.set_image(url=json['url'])
        
        await ctx.send(embed=embed)
        
    @commands.command(
        help="Let's you reverse some text")
    async def reverse(self, ctx, *, text):
        embed = discord.Embed(title=f"Text reversed", description=f"""
Original text: {text}
<:reverse:879724816834375791> Reversed text: {text[::-1]}
        """)
        
        await ctx.send(embed=embed)

    @commands.command(
        help="OOF's the person you mentioned",
        aliases=['commitoof', 'commit_oof'])
    async def oof(self, ctx, member : discord.Member=None):
        if member is None or member == ctx.author:
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
    
    @commands.command(help="RPG.")
    async def rpg(self, ctx):
        validAnswers1 = ['yes', 'no']
        validAnswers2 = ['fight', 'stop']
        authorName = ctx.author.name
        pensiveName = "pensive"
        authorHP = 100
        pensiveHP = 100
        pensiveMinimumDamage = 0
        pensiveMaximumDamage = 10
        authorMinimumDamage = 0
        authorMaximumDamage = 10
        message = await ctx.send(f"Start RPG? `yes/no`")
        
        def hp(argument):
            if argument == 0:
                return "▒▒▒▒▒▒▒▒▒▒ 💔"
            if argument == 10:
                return "█▒▒▒▒▒▒▒▒▒ ❤️"
            elif argument == 20:
                return "██▒▒▒▒▒▒▒▒ ❤️"
            elif argument == 30:
                return "███▒▒▒▒▒▒▒ ❤️"
            elif argument == 40:
                return "████▒▒▒▒▒▒ ❤️"
            elif argument == 50:
                return "█████▒▒▒▒▒ ❤️"
            elif argument == 60:
                return "██████▒▒▒▒ ❤️"
            elif argument == 70:
                return "███████▒▒▒ ❤️"
            elif argument == 80:
                return "████████▒▒ ❤️"
            elif argument == 90:
                return "█████████▒ ❤️"
            elif argument == 100:
                return "██████████ ❤️"
            else:
                return "▒▒▒▒▒▒▒▒▒▒ 💔"

        def check1(m):
            return m.content.lower() in validAnswers1 and m.channel.id == ctx.channel.id and m.author.id == ctx.author.id
        
        def check2(m):
            return m.content.lower() in validAnswers2 and m.channel.id == ctx.channel.id and m.author.id == ctx.author.id

        try:
            msg = await self.client.wait_for(event='message', check=check1, timeout=15)
            
        except asyncio.TimeoutError:
            return await ctx.send("It's been over 15 seconds, please try again by doing `-rpg`")
        
        else:
            if msg.content.lower() == "no":
                return await ctx.send("Okay, stopped RPG.")

            message = await ctx.send("Starting RPG...")
            
            await message.edit("Do you want to turn hard-code mode on? `yes/no`")
            
            try:
                msg = await self.client.wait_for(event='message', check=check1, timeout=15)
                
            except asyncio.TimeoutError:
                return await ctx.send("It's been over 15 seconds, please try again by doing `-rpg`.")
            
            else:
                
                if msg.content == "yes":
                    pensiveMinimumDamage = 4
                    pensiveMaximumDamage = 20
                    authorMinimumDamage = 2
                    authorMaximumDamage = 6
            
                await ctx.send("What do you want to do? `fight/stop`") # <------ this wont work cause its not inside the if statement
                
                try:
                    msg = await self.client.wait_for(event='message', check=check2, timeout=15)
                    
                except asyncio.TimeoutError:
                    return await ctx.send("It's been over 15 seconds, please try again by doing `-rpg`.")
                
                else:
                    if msg.content.lower() == "stop":
                        return await ctx.send("Okay, stopped RPG.")
                    
                    number1 = random.randint(authorMinimumDamage, authorMaximumDamage)
                    number = number1 * 10
                    pensiveHP = pensiveHP - number
                    
                    if pensiveHP < 10:
                        return await ctx.send(f"__**🎉 {authorName} WON!!! 🎉**__\nYou did `{number}` damage to {pensiveName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                    
                    await ctx.send(f"You did `{number}` damage to {pensiveName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                    
                    number1 = random.randint(pensiveMinimumDamage, pensiveMaximumDamage)
                    number = number1 * 10
                    authorHP = authorHP - number
                    
                    await asyncio.sleep(2)

                    if authorHP < 10:
                        return await ctx.send(f"__**🎉 {pensiveName} WON!!! 🎉**__\n{pensiveName} did `{number}` damage to {authorName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")

                    await ctx.send(f"{pensiveName} did `{number}` damage to {authorName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                    
                    message = await ctx.send("What do you want to do? `fight/stop`")

                    try:
                        msg = await self.client.wait_for(event='message', check=check2, timeout=15)
                        
                    except asyncio.TimeoutError:
                        return await ctx.send("It's been over 15 seconds, please try again by doing `-rpg`")
                    
                    else:
                        if msg.content.lower() == "stop":
                            return await ctx.send("Okay, stopped RPG.")
                        
                        number1 = random.randint(authorMinimumDamage, authorMaximumDamage)
                        number = number1 * 10
                        pensiveHP = pensiveHP - number
                        
                        if pensiveHP < 10:
                            return await ctx.send(f"__**🎉 {authorName} WON!!! 🎉**__\nYou did `{number}` damage to {pensiveName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                        
                        await ctx.send(f"You did `{number}` damage to {pensiveName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                        
                        number1 = random.randint(pensiveMinimumDamage, pensiveMaximumDamage)
                        number = number1 * 10
                        authorHP = authorHP - number
                        
                        await asyncio.sleep(2)

                        if authorHP < 10:
                            return await ctx.send(f"__**🎉 {pensiveName} WON!!! 🎉**__\n{pensiveName} did `{number}` damage to {authorName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")

                        await ctx.send(f"{pensiveName} did `{number}` damage to {authorName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                        
                        message = await ctx.send("What do you want to do? `fight/stop`")
                        
                        try:
                            msg = await self.client.wait_for(event='message', check=check2, timeout=15)
                            
                        except asyncio.TimeoutError:
                            return await ctx.send("It's been over 15 seconds, please try again by doing `-rpg`")
                        
                        else:
                            if msg.content.lower() == "stop":
                                return await ctx.send("Okay, stopped RPG.")
                            
                            number1 = random.randint(authorMinimumDamage, authorMaximumDamage)
                            number = number1 * 10
                            pensiveHP = pensiveHP - number
                            
                            if pensiveHP < 10:
                                return await ctx.send(f"__**🎉 {authorName} WON!!! 🎉**__\nYou did `{number}` damage to {pensiveName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                            
                            await ctx.send(f"You did `{number}` damage to {pensiveName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")