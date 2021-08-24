  	# Imports

import discord
from unidecode import unidecode
import os
import random
import datetime
import pickle
from pathlib import Path
from better_profanity import profanity as prof
import re
from discord.ext import commands, tasks
import DiscordUtils
import asyncpg

  # Variables

TOKEN = os.getenv('TOKEN')
DEFAULT_PREFIX = 'sb!'
activity = discord.Game(name="@Stealth Bot help")
status = "online"
prof.load_censor_words_from_file("/root/stealthbot/data/badwords.txt") # Loads the badwords.txt file
no_u = ['no u', 'unou', 'noou', 'noooou', 'uno'] # Loads all no u's into an array called no_u
social_category = [829418754408317029, 829418830383677510, 829419223977426962, 841398834167939073, 837348307570393218, 862072386974515210]
fun_stuff_category = [829419667873333248, 829419746843426886, 799662507484119071, 823193053531340800, 859482564477583410, 859482572677054495, 843135406589476885]
no_mic_channel = [843135406589476885]
moderated_servers = [799330949686231050]

# async def get_prefix(client, message):
#
#     if not message.guild:
#         return commands.when_mentioned_or(DEFAULT_PREFIX)(client, message)
#
#     prefix = await client.db.fetchval('SELECT prefix FROM guilds WHERE guild_id = $1', message.guild.id)
#     if not prefix:
#         prefix = DEFAULT_PREFIX
#
#     return commands.when_mentioned_or(prefix)(client, message)

async def get_prefix(client, message):
    if not message.guild:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(client, message)
    prefix = await client.db.fetchval('SELECT prefix FROM guilds WHERE guild_id = $1', message.guild.id)
    if await client.is_owner(message.author) and client.no_prefix == True:
        if prefix:
            return commands.when_mentioned_or(prefix, "")(client, message)
        else:
            return commands.when_mentioned_or(DEFAULT_PREFIX, "")(client, message)
    if not prefix:
        prefix = DEFAULT_PREFIX
    return commands.when_mentioned_or(prefix)(client ,message)

client = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all(), activity=activity, status=status, case_insensitive=True, help_command=None) # Initializes the client object
tracker = DiscordUtils.InviteTracker(client) # Initializes the tracker object
client.owner_ids = [349373972103561218, 564890536947875868]
client.launch_time = discord.utils.utcnow()
client.no_prefix = False

	# Functions and stuff

async def create_db_pool():
    credentials = {"user": "postgres",
                   "password": "1211",
                   "database": "stealthdb",
                   "host": "localhost"}

    client.db = await asyncpg.create_pool(**credentials)
    print("Connected to PostgreSQL")

    await client.db.execute("CREATE TABLE IF NOT EXISTS guilds(guild_id bigint PRIMARY KEY, prefix text);")

	# Tasks

@tasks.loop(minutes=120) # Task to notify the owners to bump the server every 120 minutes (2 hours)
async def bump(): # Makes a task called "bump"
    channel = client.get_channel(820049182860509206) # Gets the channel called "private_chat_for_meowsir_and_ender" (820049182860509206)
    await channel.send("<@596537151802572811> <@564890536947875868> DO `!d bump` RIGHT NOW OR I BREAK YOUR KNEECAP") # Tells the both owners to bump the server

@tasks.loop(minutes=5) # Task to change the VC every 5 minutes
async def change_vc(): # Makes a task called "change_vc"
    stealth_hangout = client.get_guild(799330949686231050)
    vc = client.get_channel(828651175585906759)
    await vc.edit(name=f"Members: {stealth_hangout.member_count}")

	# Events

@client.event
async def on_ready():
    #try:
        #change_status.start() # Starts the task called "change_status"
        #print("Started task: change_status") # Prints "Started task: change_status"
    #except Exception as e:
      #print("change_status task is already active therefor we can't start it again | on_ready")
    change_vc.start() # Starts the task called "change_vc"
    print("Started task: change_vc") # Prints "Started task: change_vc"
    print('-------------================----------------') # Prints some lines to make it look better
    print(f"Connected to bot: {client.user.name}") # Prints "Connected to the bot {Name of the bot}"
    print(f"Bot ID: {client.user.id}") # Prints "Bot ID {ID of the bot}"
    print('-------------================----------------') # Prints some lines to make it look better

    channel = client.get_channel(836232733126426666) # Get the channel called "stealth_logs" (836232733126426666) and store it as the variable "channel"

    embed = discord.Embed(title="Bot started", color=0x2F3136) # Creates a embed with the title being "Bot started" and the color being 0x2F3136

    await channel.send(embed=embed) # Sends the embed in the channel

    await tracker.cache_invites() # Caches the invites

client.load_extension('jishaku')


for filename in os.listdir('./cogs'): # For every file in the folder called "cogs"
    if filename.endswith('.py'): # If the file ends with .py
        client.load_extension(f'cogs.{filename[:-3]}') # Load the file as a extension/cog
        print(f'{filename[:-3]}.py has been loaded')
print('-------------================----------------')

@client.event
async def on_invite_create(invite):
    if invite.id not in moderated_servers: # If the guild ID isn't in the list of the moderated servers then:
        return # Return
    else: # If the invite wasn't created in any of those 2 servers, then:
        await tracker.update_invite_cache(invite)

@client.event
async def on_guild_join(guild):
    if guild.id not in moderated_servers: # If the guild ID isn't in the list of the moderated servers then:
        return # Return
    else: # If the bot did join a guild different than any of those ID's then:
        await tracker.update_guild_cache(guild)

@client.event
async def on_invite_delete(invite):
    if invite.id not in moderated_servers: # If the guild ID isn't in the list of the moderated servers then:
        return # Return
    else: # If the invite wasn't deleted in any of those 2 servers, then:
        await tracker.remove_invite_cache(invite)

@client.event
async def on_guild_remove(guild):
    if guild.id not in moderated_servers: # If the guild ID isn't in the list of the moderated servers then:
        return # Return
    else: # If the bot did leave a guild different than any of those ID's then:
        await tracker.remove_guild_cache(guild)

@client.event
async def on_member_join(member): # If a member joined the server then:
    if member.guild.id not in moderated_servers: # If the guild ID isn't in the list of the moderated servers then:
        return # Return
    else: # If the guild ID is in the list of moderated servers then:
        inviter = await tracker.fetch_inviter(member) # Fetches the inviter that invited the member
        channel = client.get_channel(843503882226499634) # Gets the channel called "welcome_and_goodbye" (843503882226499634) and store it as the variable "channel"
        stealth_logs = client.get_channel(836232733126426666) # Get the channel called "stealth_logs" (836232733126426666) and store it as the variable "stealth_logs"

        embed = discord.Embed(title=f"<:join:876880818616827954> Someone joined the server", colour=discord.Color.green()) # Creates a embed with the title being "Someone joined the server" and the color being "0x2F3136"
        embed.add_field(name="<:members:858326990725709854> Member name", value=f"{member}") # Adds a new field to the embed which says who joined the server
        embed.add_field(name="Invited by", value=f"{inviter}") # Adds a new field to the embed which says who the new user has been invited by
        embed.add_field(name="<:join:876880818616827954> Account created at", value=f"{discord.utils.format_dt(member.created_at, style='f')} ({discord.utils.format_dt(member.created_at, style='R')})") # Adds a new field to the embed that says when the new member joined discord

        await channel.send(embed=embed) # Sends the embed to the "welcome_and_goodbye" channel (843503882226499634)
        await stealth_logs.send(embed=embed) # Sends the embed to the "stealth_logs" channel (836232733126426666)

@client.event
async def on_member_remove(member): # If a member left the server then:
    if member.guild.id not in moderated_servers: # If the guild ID isn't in the list of the moderated servers then:
        return # Return
    else: # If the guild ID is in the list of moderated servers then:
        channel = client.get_channel(843503882226499634) # Gets the channel called "welcome_and_goodbye" (843503882226499634) and store it as the variable "channel"
        stealth_logs = client.get_channel(836232733126426666) # Get the channel called "stealth_logs" (836232733126426666) and store it as the variable "stealth_logs"

        embed = discord.Embed(title=f"<:leave:876880812061098044> Someone left the server", colour=discord.Color.red()) # Creates a embed with the title being "Someone left the server" and the color being "0x2F3136"
        embed.add_field(name="<:members:858326990725709854> Member name", value=f"{member}") # Adds a new field to the embed which says who joined the server
        embed.add_field(name="<:join:876880818616827954> Account created at", value=f"{discord.utils.format_dt(member.created_at, style='f')} ({discord.utils.format_dt(member.created_at, style='R')})") # Adds a new field to the embed that says when the new member joined discord

        await channel.send(embed=embed) # Sends the embed to the "welcome_and_goodbye" channel (843503882226499634)
        await stealth_logs.send(embed=embed) # Sends the embed to the "stealth_logs" channel (836232733126426666)

@client.event
async def on_message(message):
    if re.match("<@!?760179628122964008>", message.content) is not None:
        await message.reply("fuck off")
    if not message.guild: # If the message wasn't sent in a guild then:
        return await client.process_commands(message) # Return and process the command.
    if message.guild.id in moderated_servers:
        if len(message.content) >  500: # If the length of the message is over 500 then:
            await message.delete() # Deletes the message
            warnMessage = f"Hey {message.author.mention}! Your message was over 500 characters so I had to delete it!\n*If you think this was a mistake then please contact Ender2K89 (The owner of this bot & server)*" # String that tells the author to not send messages over 500 messages
            await message.channel.send(warnMessage, delete_after=5.0) # Sends the warnMessage and deletes it after 5 seconds
        if message.channel.id in social_category or message.channel.id in fun_stuff_category or message.channel.id in no_mic_channel: # If the message was sent in the social, fun stuff category or the no mic channel then:
            #url_regex = re.compile(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*')
            #url_regex = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
            invite_regex = re.compile(r"<?(https?:\/\/)?(www\.)?(discord\.gg|discordapp\.com\/invite)\b([-a-zA-Z0-9/]*)>?")
            link_perms_role = discord.utils.get(message.guild.roles, name="Link Perms")

            if link_perms_role in message.author.roles:
                await client.process_commands(message) # Processes commands
                return # Return (ignore)
            else:
                if invite_regex.search(message.content):
                    await message.delete() # Deletes the message
                    warnMessage = f"Hey {message.author.mention}! Sending discord invites is not allowed!" # String that tells the author to stop sending discord invites
                    await message.channel.send(warnMessage, delete_after=5.0) # Sends the warnMessage and deletes it after 5 seconds
                else: # If it didn't match then:
                    pass # I don't know what to put
    await client.process_commands(message) # Processes commands

    # Commands

@client.command(description="Reload all badwords")
@commands.has_permissions(administrator=True) # Checks if the author executing the command has the permission "administrator"
@commands.cooldown(1, 10, commands.BucketType.user) # Sets the cooldown to 10 seconds for the user executing the command
async def reload_badwords(ctx):
    await ctx.message.delete(delay=5.0) # Deletes the author's message after 5 seconds
    await ctx.send("Done!", delete_after=5.0) # Sends "Done!" and deletes it after 5 seconds
    prof.load_censor_words_from_file("data/badwords.txt") # Loads all the badwords from the badwords.txt file again which means it'll just reload them

@client.command(aliases=['eb', 'enable_bump_notifier'], description="Secret")
@commands.has_permissions(administrator=True) # Checks if the author executing the command has the permission "administrator"
@commands.cooldown(1, 10, commands.BucketType.user) # Sets the cooldown to 10 seconds for the user executing the command
async def enable_bump(ctx):
    try: # Tries to start the task "bump"
      bump.start() # Starts the task called "bump"
      await ctx.send("Successfully enabled the bump notifier!") # Sends "Successfully enabled the bump notifier!"
    except: # If something went wrong while starting the "bump" task then:
      await ctx.send("Couldn't start the task bump cause it's already active") # Sends "Couldn't start the task bump cause it's already active"

@client.command(aliases=['db', 'disable_bump_notifier'], description="Secret")
@commands.has_permissions(administrator=True) # Checks if the author executing the command has the permission "administrator"
@commands.cooldown(1, 10, commands.BucketType.user) # Sets the cooldown to 10 seconds for the user executing the command
async def disable_bump(ctx):
    try: # Tries to cancel the task "bump"
      bump.cancel() # Cancels the task called "bump"
      await ctx.send("Successfully stopped the bump notifier!") # Sends "Successfully stopped the bump notifier!"
    except: # If something went wrong while cancelling the "bump" task then:
      await ctx.send("Couldn't stop the task bump cause it's already stopped") # Sends "Couldn't stop the task bump cause it's already stopped"

@client.command(aliases=['ev', 'enable_change_vc'], description="Secret")
@commands.has_permissions(administrator=True) # Checks if the author executing the command has the permission "administrator"
@commands.cooldown(1, 10, commands.BucketType.user) # Sets the cooldown to 10 seconds for the user executing the command
async def enable_vc(ctx):
    try: # Tries to start the task "change_vc"
      change_vc.start() # Starts the task called "change_vc"
      await ctx.send("Successfully enabled the change_vc task!") # Sends "Successfully enabled the change_vc task!"
    except: # If something went wrong while starting the "change_vc" task then:
      await ctx.send("Couldn't start the task bump cause it's already active") # Sends "Couldn't start the task change_vc cause it's already active"

@client.command(aliases=['dv', 'disable_change_vc'], description="Secret")
@commands.has_permissions(administrator=True) # Checks if the author executing the command has the permission "administrator"
@commands.cooldown(1, 10, commands.BucketType.user) # Sets the cooldown to 10 seconds for the user executing the command
async def disable_vc(ctx):
    try: # Tries to start the task "change_vc"
      change_vc.cancel() # Cancels the task called "change_vc"
      await ctx.send("Successfully disabled the change_vc task!") # Sends "Successfully enabled the change_vc task!"
    except: # If something went wrong while starting the "change_vc" task then:
      await ctx.send("Couldn't stop the task bump cause it's already stopped") # Sends "Couldn't start the task change_vc cause it's already active"

client.loop.run_until_complete(create_db_pool())
client.run("NzYwMTc5NjI4MTIyOTY0MDA4.X3IScg.6nB36O_no9YxUfQqHiBD5EK5hnQ", reconnect=True) # Runs the bot with the token being the variable "TOKEN"
