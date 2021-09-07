import discord
import asyncio
import datetime
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType

class mod(commands.Cog):
    "<:staff:858326975869485077> Moderation commands"
    def __init__(self, client):
        self.client = client

    @commands.command(help="Bans the person you mention")
    @commands.check_any(commands.has_permissions(ban_members=True), commands.is_owner())
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        if member.id == ctx.author.id:
            return await ctx.repl("You can't ban yourself!")

        if isinstance(member, discord.Member):
            if member.top_role >= ctx.me.top_role:
                return await ctx.reply(ctx, "I cannot ban that member. Try moving my role to the top.")

        if reason == None or reason > 500:
            reason = "Reason was not provided or it exceeded the 500-character limit."
        await ctx.reply(f"Successfully banned `{member}` for `{reason}`")

        try:
            await member.message(f"You have been banned from {ctx.guild}\nReason: {reason}")
            await member.ban(reason=reason)

        except:
            return await member.ban(reason=reason)

    @commands.command(help="Kicks the person you mention")
    @commands.check_any(commands.has_permissions(kick_members=True), commands.is_owner())
    @commands.bot_has_permissions(send_messages=True, embed_links=True, kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        if member.id == ctx.author.id:
            return await ctx.repl("You can't kick yourself!")

        if isinstance(member, discord.Member):
            if member.top_role >= ctx.me.top_role:
                return await ctx.reply(ctx, "I cannot kick that member. Try moving my role to the top.")

        if reason == None or reason > 500:
            reason = "Reason was not provided or it exceeded the 500-character limit."
        await ctx.reply(f"Successfully kicked `{member}` for `{reason}`")

        try:
            await member.message(f"You have been kicked from {ctx.guild}\nReason: {reason}")
            await member.kick(reason=reason)

        except:
            return await member.kick(reason=reason)

    @commands.command(help="Bulk deletes a certain amount of messages", aliases=['purge', 'cls', 'clr'])
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    async def clear(self, ctx, amount : int, channel : discord.TextChannel=None):
        if amount > 1000:
            return await ctx.reply("Amount cannot be more than 1000.")

        if channel == None:
            channel = ctx.channel

        await channel.purge(limit=amount)
        await ctx.reply(f"Successfully deleted `{amount}` messages in {channel}", delete_after=5.0)
        await ctx.message.delete()


def setup(client):
    client.add_cog(mod(client))
