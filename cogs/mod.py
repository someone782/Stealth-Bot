import discord
import datetime
import helpers
from discord.ext import commands

class mod(commands.Cog):
    "Commands that are useful for staff members"
    def __init__(self, client):
        self.client = client

    @commands.command(help="Bans the person you mentioned", aliases=['b'])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        if reason == None:
            reason = "Reason not specificed or it was over the 150-character limit."
        await ctx.reply(f"Successfully banned {member} for `{reason}`", mention_author=False, delete_after=5.0)
        try:
            await member.send(f"You've been banned from `{ctx.guild}` for `{reason}`")
            await member.ban(reason=reason)
        except:
            await member.ban(reason=reason)

    @commands.command(help="Kicks the person you mentioned", aliases=['k'])
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        if reason == None:
            reason = "Reason not specificed or it was over the 150-character limit."
        await ctx.reply(f"Successfully kicked {member} for `{reason}`", mention_author=False, delete_after=5.0)
        try:
            await member.send(f"You've been kicked from `{ctx.guild}` for `{reason}`")
            await member.kick(reason=reason)
        except:
            await member.kick(reason=reason)

def setup(client):
    client.add_cog(mod(client))
