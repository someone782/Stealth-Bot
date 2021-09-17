import discord
import helpers
import aiohttp
import datetime
from discord.ext import commands
import random

def setup(client):
    client.add_cog(animals(client))

class animals(commands.Cog):
    "🐶 Commands that show you pictures of certain animals & facts about them"
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def waifu(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.hori.ovh/sfw/waifu/')
            json = await request.json()
            
         over_18 = "No"
         if json['is_over18'] == "true":
            over_18 = "Yes"

        embed = discord.Embed(title="Waifu", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_image(url=json['url'])
        embed.set_footer(text=f"🔞 Over 18?: {over_18}")        
        
        await ctx.reply(embed=embed)


    @commands.command(help="🐱 Shows a picture of a cat and a random fact about cats")
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/cat')
            dogjson = await request.json()
            request2 = await session.get('https://some-random-api.ml/facts/cat')
            factjson = await request2.json()

        embed = discord.Embed(title="Meow", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_image(url=dogjson['link'])
        embed.set_footer(text=factjson['fact'])
        await ctx.reply(embed=embed)

    @commands.command(help="🐶 Shows a picture of a dog and a random fact about dogs")
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def dog(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/dog')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/dog')
          factjson = await request2.json()

       embed = discord.Embed(title="Woof", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed)

    @commands.command(help="🐶 Sends you a random picture of a shiba")
    async def shiba(self, ctx):
        subreddit = "shiba"
        url = f"https://reddit.com/r/{subreddit}/random.json?limit=1"

        async with self.client.session.get(f"https://reddit.com/r/{subreddit}/random.json?limit=1") as r:
            res = await r.json()
            s = ""
            try:
                subredditDict = dict(res[0]['data']['children'][0]['data'])
            except KeyError:
                return await ctx.send("I couldn't find that subreddit.")
            embed = discord.Embed(title=f"{subredditDict['title']}", url=f"https://reddit.com{subredditDict['permalink']}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_image(url=subredditDict['url'])
            embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @commands.command(help="🐼 Shows a picture of a panda and a random fact about pandas")
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def panda(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/panda')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/panda')
          factjson = await request2.json()

       embed = discord.Embed(title="Panda!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed)

    @commands.command(help="🦊 Shows a picture of a fox and a random fact about foxes")
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def fox(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/fox')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/fox')
          factjson = await request2.json()

       embed = discord.Embed(title="Fox!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed)

    @commands.command(help="🐦 Shows a picture of a bird and a random fact about birds")
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def bird(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/bird')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/bird')
          factjson = await request2.json()

       embed = discord.Embed(title="Bird!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed)

    @commands.command(help="🐨 Shows a picture of a koala and a random fact about koalas")
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def koala(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/koala')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/koala')
          factjson = await request2.json()

       embed = discord.Embed(title="Koala!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed)

    @commands.command(help="🦘 Shows a picture of a kangaroo and a random fact about kangaroos")
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def kangaroo(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/kangaroo')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/kangaroo')
          factjson = await request2.json()

       embed = discord.Embed(title="Kangaroo!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed)

    @commands.command(help="🦝 hows a picture of a raccoon and a random fact about raccoons")
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def raccoon(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/racoon')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/racoon')
          factjson = await request2.json()

       embed = discord.Embed(title="Racoon!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed)

    @commands.command(help="🐳 Shows a picture of a whale and a random fact about whales", aliases=['urmom', 'ur_mom', 'yourmom', 'your_mom'])
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def whale(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/whale')
          dogjson = await request.json()
          request2 = await session.get('https://some-random-api.ml/facts/whale')
          factjson = await request2.json()

       embed = discord.Embed(title="Whale!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       embed.set_footer(text=factjson['fact'])
       await ctx.reply(embed=embed)

    @commands.command(help="Shows a picture of a pikachu")
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def pikachu(self, ctx):
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/pikachu')
          dogjson = await request.json()

       embed = discord.Embed(title="Pikachu!", timestamp=discord.utils.utcnow(), color=0x2F3136)
       embed.set_image(url=dogjson['link'])
       await ctx.reply(embed=embed)
