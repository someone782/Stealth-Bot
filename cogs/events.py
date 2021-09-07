import discord
from discord.ext import commands
from discord.ext.commands.core import command
from discord.utils import get
from afks import afks

def remove(afk):
    if "[AFK]" in afk.split():
        return " ".join(afk.split()[1:])
    else:
        return afk

class events(commands.Cog):
    def __init__(self, client):
        self.hidden = True
        self.client = client


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content in [f'<@!{self.client.user.id}>', f'<@{self.client.user.id}>']:
            await message.reply(f"fuck off")
        if message.author.id in afks.keys():
            afks.pop(message.author.id)
            try:
                await message.author.edit(nick=remove(message.author.display_name))
            except:
                pass
            await message.channel.send(f"Welcome back {message.author.mention}, I've removed your AFK status.")

        for id, reason in afks.items():
            member = get(message.guild.members, id = id)
            if (message.reference and member == (await message.channel.fetch_message(message.reference.message_id)).author) or member.id in message.raw_mentions:
                if message.author.id == 760179628122964008:
                    return
                else:
                    await message.reply(f"{member.name} is AFK for {reason}.")

    @commands.Cog.listener()
    async def on_guid_join(self, guild):
        channel = self.client.get_channel(883658687867158529)
        embed = discord.Embed(title="I've been added to a guild", description=f"Guild name: {guild.name}\nGuild ID: {guild.id}", timestamp=discord.utils.utcnow(), color=0x2F3136)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guid_remove(self, guild):
        channel = self.client.get_channel(883658687867158529)
        embed = discord.Embed(title="I've been removed from a guild", description=f"Guild name: {guild.name}\nGuild ID: {guild.id}", timestamp=discord.utils.utcnow(), color=0x2F3136)

        await channel.send(embed=embed)


def setup(client):
    client.add_cog(events(client))
