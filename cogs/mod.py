import discord
import asyncio
import typing
import itertools
from collections import Counter
import random
import re
import errors
import datetime
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType
from discord.ext.menus.views import ViewMenuPages

def setup(client):
    client.add_cog(Mod(client))

class ServerBansEmbedPage(menus.ListPageSource):
    def __init__(self, data, guild):
        self.data = data
        self.guild = guild
        super().__init__(data, per_page=20)
        
    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        bans = await self.guild.bans()
        embed = discord.Embed(title=f"{self.guild}'s bans ({len(bans)})", description="\n".join(f'{i+1}. {v}' for i, v in enumerate(entries, start=offset)), timestamp=discord.utils.utcnow(), color=color)
        return embed

class Mod(commands.Cog):
    "<:staff:858326975869485077> | Moderation commands"
    def __init__(self, client):
        self.client = client
        
    @staticmethod
    async def do_removal(ctx: commands.Context, limit: int, predicate, *, before=None, after=None, bulk: bool = True):
        if limit > 2000:
            return await ctx.send(f'Too many messages to search given ({limit}/2000)')

        async with ctx.typing():
            if before is None:
                before = ctx.message
            else:
                before = discord.Object(id=before)

            if after is not None:
                after = discord.Object(id=after)

            try:
                deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate, bulk=bulk)
            except discord.Forbidden:
                return await ctx.send('I do not have permissions to delete messages.')
            except discord.HTTPException as e:
                return await ctx.send(f'Error: {e} (try a smaller search?)')

            spammers = Counter(m.author.display_name for m in deleted)
            deleted = len(deleted)
            messages = [f'{deleted} message{" was" if deleted == 1 else "s were"} removed.']
            if deleted:
                messages.append('')
                spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
                messages.extend(f'**{name}**: {count}' for name, count in spammers)

            to_send = '\n'.join(messages)

            if len(to_send) > 2000:
                await ctx.send(f'Successfully removed {deleted} messages.', delete_after=10, reply=False)
            else:
                await ctx.send(to_send, delete_after=10, reply=False)
        
    @commands.command(help="Cleans up the bots messages.")
    async def cleanup(self, ctx, amount : int=25):
        if amount > 25:
            
            if not ctx.channel.permissions_for(ctx.author).manage_messages:
                return await ctx.send("You must have `manage_messages` permission to perform a search greater than 25")
            
            if not ctx.channel.permissions_for(ctx.me).manage_messages:
                return await ctx.send("I need the `manage_messages` permission to perform a search greater than 25")

        if ctx.channel.permissions_for(ctx.me).manage_messages:
            prefix = tuple(await self.client.get_pre(self.client, ctx.message))
            bulk = True

            def check(msg):
                return msg.author == ctx.me or msg.content.startswith(prefix)
        else:
            bulk = False

            def check(msg):
                return msg.author == ctx.me

        await self.do_removal(ctx, predicate=check, bulk=bulk, limit=amount)

    @commands.command(help="Gets the current guild's list of bans")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bans(self, ctx, id : int=None):
        if id:
            guild = self.client.get_guild(id)
            if not guild:
                return await ctx.send("I couldn't find that server. Make sure the ID you entered was correct.")
        else:
            guild = ctx.guild
            
        guildBans = await guild.bans()
        bans = []
        
        if not guildBans:
            raise errors.NoBannedMembers
        
        for ban in guildBans:
            
            bans.append(f"{ban.user}")
            
        paginator = ViewMenuPages(source=ServerBansEmbedPage(bans,guild), clear_reactions_after=True)
        page = await paginator._source.get_page(0)
        kwargs = await paginator._get_kwargs_from_page(page)
        if paginator.build_view():
            paginator.message = await ctx.send(embed=kwargs['embed'],view = paginator.build_view())
        else:
            paginator.message = await ctx.send(embed=kwargs['embed'])
        await paginator.start(ctx)

    @commands.command()
    async def punish(self, ctx):
        valid_punishments = ['kick', 'ban']

        def check(m: discord.Message):  # m = discord.Message.
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        message = await ctx.send("What do you want the punishment to be? (kick/ban)")

        try:
            punishment = await self.client.wait_for(event='message', timeout=15, check=check)
        except asyncio.TimeoutError:
            await message.delete()
            await ctx.message.delete(delay=5.0)
            return await ctx.send("It's been over 15 seconds, please try again by doing `-punish`", delete_after=5.0)
        else:
            await ctx.send("Who do you want me to punish?")

            try:
                member = await self.client.wait_for(event='message', timeout=15, check=check)
            except asyncio.TimeoutError:
                await message.delete()
                await ctx.message.delete(delay=5.0)
                return await ctx.send("It's been over 15 seconds, please try again by doing `-punish`", delete_after=5.0)
            else:
                    await ctx.send("What's the reason for this punishment?")

                    try:
                        reason = await self.client.wait_for(event='message', timeout=15, check=check)
                    except asyncio.TimeoutError:
                        await message.delete()
                        await ctx.message.delete(delay=5.0)
                        return await ctx.send("It's been over 15 seconds, please try again by doing `-punish`", delete_after=5.0)
                    else:
                        await ctx.send(f"{punishment.content} {member.content} {reason.content}")

                        punishment = punishment.content
                        member = commands.MemberConverter().convert(ctx, member.content)
                        reason = reason.content

                        if punishment not in valid_punishments:
                            return await ctx.send(f"That's not a valid punishment. Please try again by doing `-punish`.")

                        if reason > 500:
                            return await ctx.send(f"Your reason has exceeded the 500-character limit. Please try again by doing `-punish`")

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
                return await ctx.send(ctx, "I cannot ban that member. Try moving my role to the top.")

        if reason == None or reason > 500:
            reason = "Reason was not provided or it exceeded the 500-character limit."
        await ctx.send(f"Successfully banned `{member}` for `{reason}`")

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
                return await ctx.send(ctx, "I cannot kick that member. Try moving my role to the top.")

        if reason == None or reason > 500:
            reason = "Reason was not provided or it exceeded the 500-character limit."
        await ctx.send(f"Successfully kicked `{member}` for `{reason}`")

        try:
            await member.message(f"You have been kicked from {ctx.guild}\nReason: {reason}")
            await member.kick(reason=reason)

        except:
            return await member.kick(reason=reason)

    @commands.command(help="Bulk deletes a certain amount of messages", aliases=['cls', 'clr'])
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    async def purge(self, ctx, amount : int, channel : discord.TextChannel=None):
        if amount > 1000:
            return await ctx.send("Amount cannot be more than 1000.")

        if channel == None:
            channel = ctx.channel

        text = 'messages'
        if amount == 1:
            text = 'message'

        await ctx.message.delete()
        await channel.purge(limit=amount)
        await ctx.send(f"Successfully deleted `{amount}` {text} in {channel.mention}.", delete_after=5.0)


    @commands.command(help="Changes the slowmode of a channel", aliases=['sm', 'slowm', 'slowness'])
    @commands.check_any(commands.has_permissions(manage_channels=True), commands.is_owner())
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_channels=True)
    async def slowmode(self, ctx, number : int, channel : discord.TextChannel=None):
        if number > 21600:
            return await ctx.send("Number cannot be more than 21600.")

        if channel == None:
            channel = ctx.channel

        await channel.edit(slowmode_delay=number, reason=f'Changed by `{ctx.author}`  using command')
        await ctx.send(f"Successfully changed the slowmode of {channel.mention} to `{number}`.", delete_after=5.0)
        await ctx.message.delete()

    @commands.command(help="Creates a new role", aliases=['create_role', 'addrole', 'add_role',' newrole', 'new_role'])
    @commands.check_any(commands.has_permissions(manage_roles=True), commands.is_owner())
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_roles=True)
    async def createrole(self, ctx, color : discord.Color, *, name):
        server = ctx.guild

        await server.create_role(name=name, color=color, reason=f'Made by `{ctx.author}` using command')
        await ctx.send(f"Successfully created a role called `{name}` with the color being `{color}`.")
