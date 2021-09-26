from typing import TYPE_CHECKING
import discord
import helpers
import time
import aiohttp
import datetime
from discord.ext import commands
import random


def setup(client):
    client.add_cog(Images(client))
    
class Images(commands.Cog):
   ":frame_photo: | Commands that show you images?..."
   def __init__(self, client):
      self.client = client
      
   @commands.command(aliases=['sfw_waifu', 'waifu_sfw'])
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def waifu(self, ctx, type : str=None):
      url = "https://api.waifu.im/sfw/waifu/"
      
      if str(type).lower() == "gif":
         url = "https://api.waifu.im/sfw/waifu/?gif=True"
         
      start = time.perf_counter()
         
      request = await self.client.session.get(url)
      json = await request.json()

      end = time.perf_counter()
      
      ms = (end - start) * 1000
         
      dominant_color1 = str(json['dominant_color']).replace('#', '')
      dominant_color = int(dominant_color1, 16)

      embed = discord.Embed(title="Waifu", url=json['url'], timestamp=discord.utils.utcnow(), color=dominant_color)
      embed.set_image(url=json['url'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))}", icon_url=ctx.author.avatar.url)

      await ctx.reply(embed=embed)
      
   @commands.command(aliases=['sfw_maid', 'maid_sfw'])
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def maid(self, ctx, type : str=None):
      url = "https://api.waifu.im/sfw/maid/"
      
      if str(type).lower() == "gif":
         url = "https://api.waifu.im/sfw/maid/?gif=True"
         
      start = time.perf_counter()
         
      request = await self.client.session.get(url)
      json = await request.json()

      end = time.perf_counter()
      
      ms = (end - start) * 1000
         
      dominant_color1 = str(json['dominant_color']).replace('#', '')
      dominant_color = int(dominant_color1, 16)

      embed = discord.Embed(title="Maid", url=json['url'], timestamp=discord.utils.utcnow(), color=dominant_color)
      embed.set_image(url=json['url'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))}", icon_url=ctx.author.avatar.url)

      await ctx.reply(embed=embed)
      
   @commands.command(help="🐶 Shows a picture of a shiba", aliases=['shibe'])
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def shiba(self, ctx):
      start = time.perf_counter()
         
      request = await self.client.session.get('https://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true')
      json = await request.json()

      end = time.perf_counter()
      
      ms = (end - start) * 1000
      
      titles = ["Bark!", "Arf!", "Woof!", "Bork!"]

      embed = discord.Embed(title=f"{random.choice(titles)}", url=json[0])
      embed.set_image(url=json[0])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))}", icon_url=ctx.author.avatar.url)
      
      await ctx.send(embed=embed)
      
   @commands.command(help="Shows a picture of a axolotl and a random fact about axolotls")
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def axolotl(self, ctx):
      start = time.perf_counter()
         
      request = await self.client.session.get('https://axoltlapi.herokuapp.com/')
      json = await request.json()

      end = time.perf_counter()
      
      ms = (end - start) * 1000

      embed = discord.Embed(title="Axolotl", url=json['url'])
      embed.set_image(url=json['url'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))} • {json['facts']}")
      
      await ctx.send(embed=embed)

   @commands.command(help="🐱 Shows a picture of a cat and a random fact about cats")
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def cat(self, ctx):
      start = time.perf_counter()
         
      request = await self.client.session.get('https://some-random-api.ml/img/cat')
      pictureJson = await request.json()
      request2 = await self.client.session.get('https://some-random-api.ml/facts/cat')
      factJson = await request2.json()
      
      end = time.perf_counter()
      
      ms = (end - start) * 1000

      embed = discord.Embed(title="Meow", url=pictureJson['link'])
      embed.set_image(url=pictureJson['link'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))} • {factJson['fact']}", icon_url=ctx.author.avatar.url)
      
      await ctx.send(embed=embed)

   @commands.command(help="🐶 Shows a picture of a dog and a random fact about dogs")
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def dog(self, ctx):
      start = time.perf_counter()
      
      request = await self.client.session.get('https://some-random-api.ml/img/dog')
      pictureJson = await request.json()
      request2 = await self.client.session.get('https://some-random-api.ml/facts/dog')
      factJson = await request2.json()
      
      end = time.perf_counter()
      
      ms = (end - start) * 1000
      
      titles = ["Bark!", "Arf!", "Woof!", "Bork!"]

      embed = discord.Embed(title=f"{random.choice(titles)}", url=pictureJson['link'])
      embed.set_image(url=pictureJson['link'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))} • {factJson['fact']}", icon_url=ctx.author.avatar.url)
      
      await ctx.send(embed=embed)

   @commands.command(help="🐼 Shows a picture of a panda and a random fact about pandas")
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def panda(self, ctx):
      start = time.perf_counter()
         
      request = await self.client.session.get('https://some-random-api.ml/img/panda')
      pictureJson = await request.json()
      request2 = await self.client.session.get('https://some-random-api.ml/facts/panda')
      factJson = await request2.json()
      
      end = time.perf_counter()
      
      ms = (end - start) * 1000

      embed = discord.Embed(title="Panda!", url=pictureJson['link'])
      embed.set_image(url=pictureJson['link'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))} • {factJson['fact']}", icon_url=ctx.author.avatar.url)
      
      await ctx.send(embed=embed)

   @commands.command(help="🦊 Shows a picture of a fox and a random fact about foxes")
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def fox(self, ctx):
      start = time.perf_counter()
         
      request = await self.client.session.get('https://some-random-api.ml/img/fox')
      pictureJson = await request.json()
      request2 = await self.client.session.get('https://some-random-api.ml/facts/fox')
      factJson = await request2.json()
      
      end = time.perf_counter()
      
      ms = (end - start) * 1000

      embed = discord.Embed(title="Fox!", url=pictureJson['link'])
      embed.set_image(url=pictureJson['link'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))} • {factJson['fact']}", icon_url=ctx.author.avatar.url)
      
      await ctx.send(embed=embed)

   @commands.command(help="🐦 Shows a picture of a bird and a random fact about birds")
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def bird(self, ctx):
      request = await self.client.session.get('https://some-random-api.ml/img/bird')
      pictureJson = await request.json()
      request2 = await self.client.session.get('https://some-random-api.ml/facts/bird')
      factJson = await request2.json()
      
      end = time.perf_counter()
      
      ms = (end - start) * 1000

      embed = discord.Embed(title="Bird!", url=pictureJson['link'])
      embed.set_image(url=pictureJson['link'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))} • {factJson['fact']}", icon_url=ctx.author.avatar.url)
      
      await ctx.send(embed=embed)

   @commands.command(help="🐨 Shows a picture of a koala and a random fact about koalas")
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def koala(self, ctx):
      start = time.perf_counter()
         
      request = await self.client.session.get('https://some-random-api.ml/img/koala')
      pictureJson = await request.json()
      request2 = await self.client.session.get('https://some-random-api.ml/facts/koala')
      factJson = await request2.json()
      
      end = time.perf_counter()
      
      ms = (end - start) * 1000

      embed = discord.Embed(title="Koala!", url=pictureJson['link'])
      embed.set_image(url=pictureJson['link'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))} • {factJson['fact']}", icon_url=ctx.author.avatar.url)
      
      await ctx.send(embed=embed)

   @commands.command(help="🦘 Shows a picture of a kangaroo and a random fact about kangaroos")
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def kangaroo(self, ctx):
      start = time.perf_counter()
         
      request = await self.client.session.get('https://some-random-api.ml/img/kangaroo')
      pictureJson = await request.json()
      request2 = await self.client.session.get('https://some-random-api.ml/facts/kangaroo')
      factJson = await request2.json()
      
      end = time.perf_counter()
      
      ms = (end - start) * 1000

      embed = discord.Embed(title="Kangaroo!", url=pictureJson['link'])
      embed.set_image(url=pictureJson['link'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))} • {factJson['fact']}", icon_url=ctx.author.avatar.url)
      
      await ctx.send(embed=embed)

   @commands.command(help="🦝 Shows a picture of a raccoon and a random fact about racoons", aliases=['raccoon'])
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def racoon(self, ctx):
      start = time.perf_counter()
         
      request = await self.client.session.get('https://some-random-api.ml/img/racoon')
      pictureJson = await request.json()
      request2 = await self.client.session.get('https://some-random-api.ml/facts/racoon')
      factJson = await request2.json()
      
      end = time.perf_counter()
      
      ms = (end - start) * 1000

      embed = discord.Embed(title="Racoon!", url=pictureJson['link'])
      embed.set_image(url=pictureJson['link'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))} • {factJson['fact']}", icon_url=ctx.author.avatar.url)
      
      await ctx.send(embed=embed)

   @commands.command(help="🐳 Shows a picture of a whale and a random fact about whales", aliases=['urmom', 'ur_mom', 'yourmom', 'your_mom'])
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def whale(self, ctx):
      start = time.perf_counter()
         
      request = await self.client.session.get('https://some-random-api.ml/img/whale')
      pictureJson = await request.json()
      request2 = await self.client.session.get('https://some-random-api.ml/facts/whale')
      factJson = await request2.json()
      
      end = time.perf_counter()
      
      ms = (end - start) * 1000

      embed = discord.Embed(title="Whale!", url=pictureJson['link'])
      embed.set_image(url=pictureJson['link'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))} • {factJson['fact']}", icon_url=ctx.author.avatar.url)
      
      await ctx.send(embed=embed)

   @commands.command(help="Shows a picture of a pikachu")
   @commands.bot_has_permissions(send_messages=True, embed_links=True)
   async def pikachu(self, ctx):
      start = time.perf_counter()
         
      request = await self.client.session.get('https://some-random-api.ml/img/pikachu')
      pictureJson = await request.json()
      
      end = time.perf_counter()
      
      ms = (end - start) * 1000

      embed = discord.Embed(title="Pikachu!", url=pictureJson['link'])
      embed.set_image(url=pictureJson['link'])
      embed.set_footer(text=f"{round(ms)}ms{'' * (9-len(str(round(ms, 3))))}", icon_url=ctx.author.avatar.url)
      
      await ctx.send(embed=embed)