import discord
import datetime
import aiohttp
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType

def setup(client):
    client.add_cog(nsfw(client))

class nsfw(commands.Cog):
    ":underage: NSFW commands"
    def __init__(self, client):
        self.client = client

    @commands.command(help="Shows you a random post from the subreddit r/hentai")
    @commands.is_nsfw()
    async def hentai(self, ctx):
        subreddit = "hentai"
        url = f"https://reddit.com/r/{subreddit}/random.json?limit=1"

        async with self.client.session.get(f"https://reddit.com/r/{subreddit}/random.json?limit=1") as r:
            res = await r.json()
            subredditDict = dict(res[0]['data']['children'][0]['data'])
            embed = discord.Embed(title=f"{subredditDict['title']}", url=f"https://reddit.com{subredditDict['permalink']}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_image(url=subredditDict['url'])
            embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed)

    @commands.command(help="Shows you a random post from the subreddit r/HENTAI_GIF", aliases=['hentaigif'])
    @commands.is_nsfw()
    async def hentai_gif(self, ctx):
        subreddit = "HENTAI_GIF"
        url = f"https://reddit.com/r/{subreddit}/random.json?limit=1"

        async with self.client.session.get(f"https://reddit.com/r/{subreddit}/random.json?limit=1") as r:
            res = await r.json()
            subredditDict = dict(res[0]['data']['children'][0]['data'])
            embed = discord.Embed(title=f"{subredditDict['title']}", url=f"https://reddit.com{subredditDict['permalink']}", timestamp=discord.utils.utcnow(), color=0x2F3136)
            embed.set_image(url=subredditDict['url'])
            embed.set_footer(text=f"Command requested by: {ctx.author}", icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed)
