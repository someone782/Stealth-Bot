import discord
import datetime
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType

class mod(commands.Cog):
    "Moderation commands"
    def __init__(self, client):
        self.client = client

    @commands.command(help="Bans the person you mention")
    @commands.bot_has_permissions()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        if reason == None or reason > 500:
            reason = "Reason was not provided or it exceeded the 500-character limit."


def setup(client):
    client.add_cog(mod(client))
