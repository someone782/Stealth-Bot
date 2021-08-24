import discord
import helpers
import aiohttp
import datetime
from discord.ext import commands
import random

class animals(commands.Cog):
    "Commands that show you pictures of certain animals & facts about them"
    def __init__(self, client):
        self.client = client


    @commands.command(help="Shows a picture of a cat and a random fact about cats")
    async def cat(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/cat')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/cat')
          factjson = await request2.json()

       embed = discord.Embed(title="Meow", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed, mention_author=False)

    @commands.command(help="Shows a picture of a dog and a random fact about dogs")
    async def dog(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/dog')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/dog')
          factjson = await request2.json()

       embed = discord.Embed(title="Woof", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed, mention_author=False)

    @commands.command(description="Shows you a random shiba from Reddit.")
    async def shiba(self, ctx):
        epic = random.random()
        if epic > 0.5:
            URL = "https://www.reddit.com/r/shiba/hot.json?limit=102"
        else:
            URL = "https://www.reddit.com/r/shiba/hot.json?limit=102"



        async with aiohttp.request("GET", URL) as something:
            if something.status == 200:
                json_data = await something.json()
                radome = random.randint(0, 100)
                image = json_data["data"]["children"][radome]["data"]["url"]
                embed = discord.Embed(title="Woof", timestamp=discord.utils.utcnow(), color=0x2F3136)
                embed.set_image(url=image)
                embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

                await ctx.reply(embed=embed, mention_author=False)
            else:
                print(f"The request was invalid\nStatus code: {something.status}")
                return await ctx.reply(f"Something went wrong!`", mention_author=False)

    @commands.command(help="Shows a picture of a panda and a random fact about pandas")
    async def panda(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/panda')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/panda')
          factjson = await request2.json()

       embed = discord.Embed(title="Panda!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed, mention_author=False)

    @commands.command(help="Shows a picture of a fox and a random fact about foxes")
    async def fox(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/fox')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/fox')
          factjson = await request2.json()

       embed = discord.Embed(title="Fox!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed, mention_author=False)

    @commands.command(help="Shows a picture of a bird and a random fact about birds")
    async def bird(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/bird')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/bird')
          factjson = await request2.json()

       embed = discord.Embed(title="Bird!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed, mention_author=False)

    @commands.command(help="Shows a picture of a koala and a random fact about koalas")
    async def koala(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/koala')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/koala')
          factjson = await request2.json()

       embed = discord.Embed(title="Koala!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed, mention_author=False)

    @commands.command(help="Shows a picture of a kangaroo and a random fact about kangaroos")
    async def kangaroo(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/kangaroo')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/kangaroo')
          factjson = await request2.json()

       embed = discord.Embed(title="Kangaroo!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed, mention_author=False)

    @commands.command(help="Shows a picture of a racoon and a random fact about racoons")
    async def racoon(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/racoon')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/racoon')
          factjson = await request2.json()

       embed = discord.Embed(title="Racoon!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed, mention_author=False)

    @commands.command(help="Shows a picture of a whale and a random fact about whales", aliases=['urmom', 'ur_mom', 'yourmom', 'your_mom'])
    async def whale(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/whale')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/whale')
          factjson = await request2.json()

       embed = discord.Embed(title="Whale!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed, mention_author=False)

    @commands.command(help="Shows a picture of a pikachu")
    async def pikachu(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/pikachu')
          dogjson = await request.json()

       embed = discord.Embed(title="Pikachu!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       await ctx.reply(embed=embed, mention_author=False)


def setup(client):
    client.add_cog(animals(client))
