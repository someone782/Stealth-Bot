import discord
import datetime
import aiohttp
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType

def setup(client):
    client.add_cog(NSFW(client))

class NSFW(commands.Cog):
    "🔞 NSFW commands"
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['nsfw_ass', 'ass_nsfw'])
    @commands.is_nsfw()
    async def ass(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.waifu.im/nsfw/ass/')
            json = await request.json()
            
        print(str(json['dominant_color']).replace('#', ''))
        

        embed = discord.Embed(title="Ass")
        embed.set_image(url=json['url'])

        await ctx.send(embed=embed)
        
    @commands.command(aliases=['nsfw_ecchi', 'ecchi_nsfw'])
    @commands.is_nsfw()
    async def ecchi(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.waifu.im/nsfw/ecchi/')
            json = await request.json()

        embed = discord.Embed(title="Ecchi")
        embed.set_image(url=json['url'])

        await ctx.send(embed=embed)
        
    @commands.command(aliases=['nsfw_ero', 'ero_nsfw'])
    @commands.is_nsfw()
    async def ero(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.waifu.im/nsfw/ero/')
            json = await request.json()

        embed = discord.Embed(title="Ero")
        embed.set_image(url=json['url'])

        await ctx.send(embed=embed)
        
    @commands.command(aliases=['nsfw_hentai', 'hentai_nsfw'])
    @commands.is_nsfw()
    async def hentai(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.waifu.im/nsfw/hentai/')
            json = await request.json()

        embed = discord.Embed(title="Hentai")
        embed.set_image(url=json['url'])

        await ctx.send(embed=embed)
        
    @commands.command(aliases=['nsfw_maid', 'maid_nsfw'])
    @commands.is_nsfw()
    async def maid(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.waifu.im/nsfw/maid/')
            json = await request.json()

        embed = discord.Embed(title="Maid")
        embed.set_image(url=json['url'])

        await ctx.send(embed=embed)

    @commands.command(aliases=['nsfw_milf', 'milf_nsfw'])
    @commands.is_nsfw()
    async def milf(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.waifu.im/nsfw/milf/')
            json = await request.json()

        embed = discord.Embed(title="Milf")
        embed.set_image(url=json['url'])

        await ctx.send(embed=embed)

    @commands.command(aliases=['nsfw_oppai', 'oppai_nsfw'])
    @commands.is_nsfw()
    async def oppai(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.waifu.im/nsfw/oppai/')
            json = await request.json()

        embed = discord.Embed(title="Oppai")
        embed.set_image(url=json['url'])

        await ctx.send(embed=embed)

    @commands.command(aliases=['nsfw_oral', 'oral_nsfw'])
    @commands.is_nsfw()
    async def oral(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.waifu.im/nsfw/oral/')
            json = await request.json()

        embed = discord.Embed(title="Oral")
        embed.set_image(url=json['url'])

        await ctx.send(embed=embed)

    @commands.command(aliases=['nsfw_paizuri', 'paizuri_nsfw'])
    @commands.is_nsfw()
    async def paizuri(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.waifu.im/nsfw/paizuri/')
            json = await request.json()

        embed = discord.Embed(title="Paizuri")
        embed.set_image(url=json['url'])

        await ctx.send(embed=embed)
        
    @commands.command(aliases=['nsfw_selfies', 'selfies_nsfw', 'selfie', 'nsfw_selfie', 'selfie_nsfw'])
    @commands.is_nsfw()
    async def selfies(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.waifu.im/nsfw/selfie/')
            json = await request.json()

        embed = discord.Embed(title="Selfie")
        embed.set_image(url=json['url'])

        await ctx.send(embed=embed)
        
    @commands.command(aliases=['nsfw_uniform', 'uniform_nsfw'])
    @commands.is_nsfw()
    async def uniform(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://api.waifu.im/nsfw/uniform/')
            json = await request.json()

        embed = discord.Embed(title="Uniform")
        embed.set_image(url=json['url'])

        await ctx.send(embed=embed)
