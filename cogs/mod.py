import discord
import asyncio
import datetime
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType

class mod(commands.Cog):
    "<:staff:858326975869485077> Moderation commands"
    def __init__(self, client):
        self.client = client

    @commands.command(help="Announces a message in a specified channel")
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def announce(self, ctx, channel : discord.TextChannel, *, message):
        channelid = channel.id
        channel = self.client.get_channel(channelid)

        try:
            await ctx.message.delete()
        except:
            pass

        await channel.send(message)

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
        await ctx.reply(f"Successfully deleted `{amount}` messages in {channel.mention}.", delete_after=5.0)
        await ctx.message.delete()

    @commands.command(help="Changes the slowmode of a channel", aliases=['sm', 'slowm', 'slowness'])
    @commands.check_any(commands.has_permissions(manage_channels=True), commands.is_owner())
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_channels=True)
    async def slowmode(self, ctx, number : int, channel : discord.TextChannel=None):
        if number > 21600:
            return await ctx.reply("Number cannot be more than 21600.")

        if channel == None:
            channel = ctx.channel

        await channel.edit(slowmode_delay=number, reason=f'Changed by `{ctx.author}`  using command')
        await ctx.reply(f"Successfully changed the slowmode of {channel.mention} to `{number}`.", delete_after=5.0)
        await ctx.message.delete()

    @commands.command(help="Creates a new role", aliases=['create_role', 'addrole', 'add_role',' newrole', 'new_role'])
    @commands.check_any(commands.has_permissions(manage_roles=True), commands.is_owner())
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_roles=True)
    async def createrole(self, ctx, color : discord.Color, *, name):
        server = ctx.guild

        await server.create_role(name=name, color=color, reason=f'Made by `{ctx.author}` using command')
        await ctx.reply(f"Successfully created a role called `{name}` with the color being `{color}`.")

def setup(client):
    client.add_cog(mod(client))
