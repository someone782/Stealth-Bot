import discord
import random
import asyncio
from discord.ext import commands

def setup(client):
    client.add_cog(Custom(client))

class Custom(commands.Cog):
    ":tada: | Commands that are made by members that won a giveaway called \"Custom command for Stealth Bot\""
    def __init__(self, client):
        self.hidden = True
        self.client = client


    # <@691733395109314661>

    @commands.command(help="Bonk.")
    async def cbonk(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author
            message = "just bonked themselves"
        else:
            message = "just got bonked by"
        await ctx.send(f"{member.mention} {message} {ctx.author.mention}. What a loser!")

    # <@547059830062448670>

    @commands.command(help="Tells you to have some pickles!")
    async def hungry(self, ctx):
        await ctx.send(f"then have some pickles!")

    # <@748105241857097759>

    @commands.command(help="Tells you to shut up cause stars is sleeping")
    async def stars(self, ctx):
        await ctx.send(f"shut up, stars is sleeping")

    # <@547059830062448670>

    @commands.command(help="Tells you if someone has good or bad luck")
    async def luck(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author
        responses = ["has bad luck!",
                    "has good luck!"]
        await ctx.send(f"{member.mention} {random.choice(responses)}")
        return

	# <@691733395109314661>

    @commands.command(aliases=["jason-derulo", "jason_derulo"], help="Replies with wiggle wiggle wiggle")
    async def jason(self, ctx):
        await ctx.send(f"Wiggle wiggle wiggle")

	# <@691733395109314661>

    @commands.command(help="Replies with she a runner she a track star")
    async def fast(self, ctx):
        await ctx.send(f"She a runner she a track star")

    # <@530472612871143476>

    @commands.command(description="Tells you if someone is weird")
    async def weird(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author
        responses = ["is weird",
                    "isn't weird"]
        await ctx.send(f"{member.mention} {random.choice(responses)}")

    # <@530472612871143476>

    @commands.command(description="Tells a fact about someone")
    async def fact(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author
        await ctx.send(f"Fun fact about {member.mention}: they're a loser.")

    # <@530472612871143476>

    @commands.command(description="Tells a lie about someone")
    async def lie(self, ctx, member : discord.Member=None):
        if(member == None):
            member = ctx.author
        await ctx.send(f"{member.mention} isn't a dissapointment")

    # <@691733395109314661>

    @commands.command(aliases=["cha_cha", "cha-cha"], description="Replies with Real smooth")
    async def cha(self, ctx):
        await ctx.send(f"Real smooth")

    # <@530472612871143476>

    @commands.command(aliases=["ping_ender", "ender_ping"], description="Pings ender, or does it..")
    async def pingender(self, ctx):
        await ctx.send(f"you thought that would work")

    # <@530472612871143476>

    @commands.command(description="Cries")
    async def cry(self, ctx):
        await ctx.send(f"😢😢😢😢😢😢😢😢😢😢")

    # <@748105241857097759>

    # @commands.command(description="Sends a GIF of a man eating a burger")
    # async def burger(self, ctx):
    #     if ctx.author.id == 555818548291829792:
    #         return await ctx.send("Sorry, but you're blacklisted from using this command.")
    #     else:
    #         await ctx.send(f"https://tenor.com/view/burger-eating-burbger-asmr-sussy-gif-21505937")

    # <@530472612871143476>

    @commands.command(description="Replies with e")
    async def e(self, ctx):
        await ctx.send(f"e")

    # <@294137889514717185>

    @commands.command(description="EA Sports")
    async def ea(self, ctx):
        await ctx.send(f"sports")

    # <@294137889514717185>

    @commands.command(description="Replies with is very slow")
    async def ffmpeg(self, ctx):
        await asyncio.sleep(15) # Waits 15 seconds
        await ctx.send(f"is very slow")

    # <@555818548291829792>

    @commands.command(description="Replies with no u")
    async def nou(self, ctx):
        await ctx.send(f"no u")

    # <@351375279698083841>

    @commands.command(description="A friendly Hello from the bot", aliases=["h"])
    async def hello(self, ctx):
        await ctx.send(f"fuck off")

    # <@699737035715641384>

    @commands.command(description="idiot")
    async def me(self, ctx):
        await ctx.send(f"fuck you")
