import discord
import datetime
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType

class mod(commands.Cog):
    "Moderation commands"
    def __init__(self, client):
        self.client = client

    @commands.command(help="Bans the person you mention")
    @commands.check_any(commands.has_permissions(ban_members=True), commands.is_owner())
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        if reason == None or reason > 500:
            reason = "Reason was not provided or it exceeded the 500-character limit."
        await ctx.reply(f"Successfully banned `{member}` for `{reason}`")

        try:
            await member.message(f"You have been banned from {ctx.guild}\nReason: {reason}")
            await member.ban(reason=reason)

        except:
            return await member.ban(reason=reason)

def setup(client):
    client.add_cog(mod(client))
