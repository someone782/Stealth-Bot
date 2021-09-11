import discord
import asyncio
import itertools
import datetime
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType

def setup(client):
    client.add_cog(mod(client))

class mod(commands.Cog):
    "<:staff:858326975869485077> Moderation commands"
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def punish(self, ctx):
        valid_punishments = ['kick', 'ban']

        def check(m: discord.Message):  # m = discord.Message.
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        await ctx.reply("What do you want the punishment to be? (kick/ban)")

        try:
            punishment = await self.client.wait_for(event='message', timeout=15, check=check)
        except asyncio.TimeoutError:
            await message.delete()
            await ctx.message.delete(delay=5.0)
            return await ctx.reply("It's been over 15 seconds, please try again by doing `-punish`", delete_after=5.0)
        else:
            await ctx.reply("Who do you want me to punish?")

            try:
                member = await self.client.wait_for(event='message', timeout=15, check=check)
            except asyncio.TimeoutError:
                await message.delete()
                await ctx.message.delete(delay=5.0)
                return await ctx.reply("It's been over 15 seconds, please try again by doing `-punish`", delete_after=5.0)
            else:
                    await ctx.reply("What's the reason for this punishment?")

                    try:
                        reason = await self.client.wait_for(event='message', timeout=15, check=check)
                    except asyncio.TimeoutError:
                        await message.delete()
                        await ctx.message.delete(delay=5.0)
                        return await ctx.reply("It's been over 15 seconds, please try again by doing `-punish`", delete_after=5.0)
                    else:
                        await ctx.reply(f"{punishment.content} {member.content} {reason.content}")

                        punishment = punishment.content
                        member = commands.MemberConverter().convert(ctx, member.content)
                        reason = reason.content

                        if punishment not in valid_punishments:
                            return await ctx.reply(f"That's not a valid punishment. Please try again by doing `-punish`.")

                        if reason > 500:
                            return await ctx.reply(f"Your reason has exceeded the 500-character limit. Please try again by doing `-punish`")

                        await member.send(f'punishment: {punishment}\nmember: {member}\n{reason}')

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
