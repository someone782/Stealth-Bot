import discord
import helpers
import aiohttp
import datetime
from discord.ext import commands
import random

def setup(client):
    client.add_cog(Images(client))
    
class Images(commands.Cog):
   "🖼️ Commands that show you images?..."
   def __init__(self, client):
      self.client = client
      
    @commands.command(aliases=['sfw_waifu', 'waifu_sfw'])
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def waifu(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.waifu.im/sfw/waifu/')
            json = await request.json()
            
        dominant_color1 = str(json['dominant_color']).replace('#', '')
        dominant_color = int(dominant_color1, 16)

        embed = discord.Embed(title="Waifu", timestamp=discord.utils.utcnow(), color=dominant_color)
        embed.set_image(url=json['url'])
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

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
      
      await ctx.send(embed=embed)

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
      
      await ctx.send(embed=embed)

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
      
      await ctx.send(embed=embed)

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
      
      await ctx.send(embed=embed)

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
      
      await ctx.send(embed=embed)

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
      
      await ctx.send(embed=embed)

   @commands.command(help="🦝 Shows a picture of a raccoon and a random fact about raccoons")
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
      
      await ctx.send(embed=embed)

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
      
      await ctx.send(embed=embed)

   @commands.command(help="Shows a picture of a pikachu")
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def pikachu(self, ctx):
      async with aiohttp.ClientSession() as session:
         request = await session.get('https://some-random-api.ml/img/pikachu')
         dogjson = await request.json()

      embed = discord.Embed(title="Pikachu!", timestamp=discord.utils.utcnow(), color=0x2F3136)
      embed.set_image(url=dogjson['link'])
      
      await ctx.send(embed=embed)