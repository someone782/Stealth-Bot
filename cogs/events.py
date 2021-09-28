import discord
from discord.ext import commands
from discord.ext.commands.core import command
from discord.utils import get
import random

def remove(afk):
    if "[AFK]" in afk.split():
        return " ".join(afk.split()[1:])
    else:
        return afk

def setup(client):
    client.add_cog(Events(client))

class Events(commands.Cog):
    "<:hypesquad_events:585765895939424258> | Just some events.. but how did you find this cog?..."
    def __init__(self, client):
        self.hidden = True
        self.client = client
        if not hasattr(self.client, 'commands_used'):
            self.client.commands_used = 0
        if not hasattr(self.client, 'messages'):
            self.client.messages = 0
        if not hasattr(self.client, 'edited_messages'):
            self.client.edited_messages = 0
        if not hasattr(self.client, 'last_message'):
            self.client.last_message = None
        if not hasattr(self.client, 'last_message_author'):
            self.client.last_message_author = None
            
    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.client.commands_used = self.client.commands_used +1
        
        commandChannel = self.client.get_channel(891644229053456424)
        
        server = ctx.guild
        channel = ctx.channel
        owner = ctx.guild.owner
        
        author = ctx.author
        
        message = ctx.message
        
        pinned = "No"
        
        if message.pinned == True:
            pinned = "Yes"
            
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        
        embed = discord.Embed(title=f"{ctx.command} has been used", description=f"""
__**Guild info**__

Name: `{server}`
ID: `{server.id}`

Channel Name: `{channel}`
Channel ID: `{channel.id}`
Channel Mention: {channel.mention}

Owner Name: `{owner}`
Owner ID: `{owner.id}`
Owner Mention: {owner.mention}
Owner Tag: `#{owner.discriminator}`

__**Author info**__

Name: `{author}`
ID: `{author.id}`
Mention: {author.mention}
Tag: `#{author.discriminator}`

__**Message info**__
URL: [Click here]({message.jump_url}/ 'Jump URL')
Content:
`{message.content}`
                              """, timestamp=discord.utils.utcnow(), color=color)
        
        await commandChannel.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        self.client.messages = self.client.messages + 1
        
        if message.author.id not in self.client.afk_users:
            return
        
        self.client.afk_users.pop(message.author.id)
        info = await self.client.db.fetchrow('SELECT * FROM afk WHERE user_id = $1', message.author.id)
        await self.client.db.execute('DELETE FROM afk WHERE user_id = $1', message.author.id)
        
        delta_uptime = discord.utils.utcnow() - info["start_time"]
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        text = f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds ({discord.utils.format_dt(info["start_time"], "R")})"
        
        colors = [0x910023, 0xA523FF]
        color = random.choice(colors)
        
        embed = discord.Embed(title=f"👋 Welcome back {message.author.name}! I've removed your AFK status.", description=f"You've been AFK for {info["reason"]}.", timestamp=discord.utils.utcnow(), color=color)
        
        await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.client.edited_messages = self.client.edited_messages + 1
        await self.client.process_commands(after)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.client.last_message = message.content
        self.client.last_message_author = message.author

    @commands.Cog.listener()
    async def on_member_join(self, member): # If a member joined the server then:
        if member.guild.id == 799330949686231050: # stealth hangout
            inviter = await self.client.tracker.fetch_inviter(member) # Fetches the inviter that invited the member
            channel = self.client.get_channel(843503882226499634) # Gets the channel called "welcome_and_goodbye" (843503882226499634) and store it as the variable "channel"
            stealth_logs = self.client.get_channel(836232733126426666) # Get the channel called "stealth_logs" (885181872777334844) and store it as the variable "stealth_logs"

            embed = discord.Embed(title=f"<:join:876880818616827954> Someone joined the server", colour=discord.Color.green()) # Creates a embed with the title being "Someone joined the server" and the color being "green"
            embed.add_field(name="<:members:858326990725709854> Member name", value=f"{member}") # Adds a new field to the embed which says who joined the server
            embed.add_field(name="Invited by", value=f"{inviter}") # Adds a new field to the embed which says who the new user has been invited by
            embed.add_field(name="<:join:876880818616827954> Account created at", value=f"{discord.utils.format_dt(member.created_at, style='f')} ({discord.utils.format_dt(member.created_at, style='R')})") # Adds a new field to the embed that says when the new member joined discord

            await channel.send(embed=embed) # Sends the embed to the "welcome_and_goodbye" channel (843503882226499634)
            await stealth_logs.send(embed=embed) # Sends the embed to the "stealth_logs" channel (885181872777334844)

        elif member.guild.id == 882341595528175686: # classicsmp
            inviter = await self.client.tracker.fetch_inviter(member) # Fetches the inviter that invited the member
            channel = self.client.get_channel(882345183813980220) # Gets the channel called "welcome_and_goodbye" (882345183813980220) and store it as the variable "channel"
            stealth_logs = self.client.get_channel(885181872777334844) # Get the channel called "stealth_logs" (885181872777334844) and store it as the variable "stealth_logs"

            embed = discord.Embed(title=f"<:join:876880818616827954> Someone joined the server", colour=discord.Color.green()) # Creates a embed with the title being "Someone joined the server" and the color being "green"
            embed.add_field(name="<:members:858326990725709854> Member name", value=f"{member}") # Adds a new field to the embed which says who joined the server
            embed.add_field(name="Invited by", value=f"{inviter}") # Adds a new field to the embed which says who the new user has been invited by
            embed.add_field(name="<:join:876880818616827954> Account created at", value=f"{discord.utils.format_dt(member.created_at, style='f')} ({discord.utils.format_dt(member.created_at, style='R')})") # Adds a new field to the embed that says when the new member joined discord

            await channel.send(embed=embed) # Sends the embed to the "welcome_and_goodbye" channel (843503882226499634)
            await stealth_logs.send(embed=embed) # Sends the embed to the "stealth_logs" channel (885181872777334844)

    @commands.Cog.listener()
    async def on_member_remove(self, member): # If a member left the server then:
        if member.guild.id == 799330949686231050: # stealth hangout
            channel = self.client.get_channel(843503882226499634) # Gets the channel called "welcome_and_goodbye" (843503882226499634) and store it as the variable "channel"
            stealth_logs = self.client.get_channel(836232733126426666) # Get the channel called "stealth_logs" (885181872777334844) and store it as the variable "stealth_logs"

            embed = discord.Embed(title=f"<:left:849392885785821224> Someone left the server", colour=discord.Color.red()) # Creates a embed with the title being "Someone joined the server" and the color being red
            embed.add_field(name="<:members:858326990725709854> Member name", value=f"{member}") # Adds a new field to the embed which says who joined the server
            embed.add_field(name="<:join:876880818616827954> Account created at", value=f"{discord.utils.format_dt(member.created_at, style='f')} ({discord.utils.format_dt(member.created_at, style='R')})") # Adds a new field to the embed that says when the new member joined discord

            await channel.send(embed=embed) # Sends the embed to the "welcome_and_goodbye" channel (843503882226499634)
            await stealth_logs.send(embed=embed) # Sends the embed to the "stealth_logs" channel (885181872777334844)

        elif member.guild.id == 882341595528175686: # classicsmp
            channel = self.client.get_channel(882345183813980220) # Gets the channel called "welcome_and_goodbye" (882345183813980220) and store it as the variable "channel"
            stealth_logs = self.client.get_channel(885181872777334844) # Get the channel called "stealth_logs" (885181872777334844) and store it as the variable "stealth_logs"

            embed = discord.Embed(title=f"<:left:849392885785821224> Someone left the server", colour=discord.Color.red()) # Creates a embed with the title being "Someone joined the server" and the color being red
            embed.add_field(name="<:members:858326990725709854> Member name", value=f"{member}") # Adds a new field to the embed which says who joined the server
            embed.add_field(name="<:join:876880818616827954> Account created at", value=f"{discord.utils.format_dt(member.created_at, style='f')} ({discord.utils.format_dt(member.created_at, style='R')})") # Adds a new field to the embed that says when the new member joined discord

            await channel.send(embed=embed) # Sends the embed to the "welcome_and_goodbye" channel (843503882226499634)
            await stealth_logs.send(embed=embed) # Sends the embed to the "stealth_logs" channel (885181872777334844)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = discord.utils.get(guild.text_channels, name='general')
        
        if not channel:
            channels = [channel for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages]
            channel = channels[0]
            
        welcomeEmbed = discord.Embed(title="Thank you for adding `Stealth Bot` to your server", description="""
We really appreciate you adding `Stealth Bot` to your server.
You can do `sb!help` to view a list of commands.""", timestamp=discord.utils.utcnow(), color=0x2F3136)
        welcomeEmbed.set_thumbnail(url=self.client.user.avatar.url)
        
        await channel.send(embed=welcomeEmbed)
        
        channel = self.client.get_channel(883658687867158529)
        embed = discord.Embed(title="I've been added to a guild", description=f"Name: {guild.name}\nID: {guild.id}\nOwner: {guild.owner.mention} **|** {guild.owner} **|** {guild.owner.id}", timestamp=discord.utils.utcnow(), color=0x2F3136)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon)
        else:
            pass
        embed.set_footer(text=f"I am now in {len(self.client.guilds)} guilds", icon_url=self.client.user.avatar.url)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.client.get_channel(883658687867158529)
        embed = discord.Embed(title="I've been removed from a guild", description=f"Name: {guild.name}\nID: {guild.id}\nOwner: {guild.owner.mention} **|** {guild.owner} **|** {guild.owner.id}", timestamp=discord.utils.utcnow(), color=0x2F3136)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon)
        else:
            pass
        embed.set_footer(text=f"I am now in {len(self.client.guilds)} guilds", icon_url=self.client.user.avatar.url)

        await channel.send(embed=embed)