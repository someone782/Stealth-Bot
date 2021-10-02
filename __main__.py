  	# Imports

import discord
import logging
from unidecode import unidecode
import os
import aiohttp
import random
import errors
from datetime import datetime
import yaml
import random
import pickle
from pathlib import Path
from better_profanity import profanity as prof
import re
from discord.ext import commands, tasks
import DiscordUtils
import asyncpg
import typing
import asyncpraw
from discord import Interaction
from typing import (
    List,
    Optional
)


with open(r'/root/stealthbot/config.yaml') as file:
    full_yaml = yaml.load(file)
yaml_data = full_yaml

PRE = ('sb!',)
activity = discord.Game(name="@Stealth Bot help")
status = "online"
prof.load_censor_words_from_file("/root/stealthbot/data/badwords.txt") # Loads the badwords.txt file
no_u = ['no u', 'unou', 'noou', 'noooou', 'uno'] # Loads all no u's into an array called no_u
social_category = [829418754408317029, 829418830383677510, 829419223977426962, 841398834167939073, 837348307570393218, 862072386974515210]
fun_stuff_category = [829419667873333248, 829419746843426886, 799662507484119071, 823193053531340800, 859482564477583410, 859482572677054495, 843135406589476885]
no_mic_channel = [843135406589476885]
moderated_servers = [799330949686231050]

# async def get_pre(client, message):
#     if not message.guild:
#         return commands.when_mentioned_or(DEFAULT_PREFIX)(client, message)
#     prefix = await client.db.fetchval('SELECT prefix FROM guilds WHERE guild_id = $1', message.guild.id)
#     if await client.is_owner(message.author) and client.no_prefix == True:
#         if prefix:
#             return commands.when_mentioned_or(prefix, "")(client, message)
#         else:
#             return commands.when_mentioned_or(DEFAULT_PREFIX, "")(client, message)
#     if not prefix:
#         prefix = DEFAULT_PREFIX
#     return commands.when_mentioned_or(prefix)(client, message)

class ConfirmButton(discord.ui.Button):
    def __init__(self, label: str, emoji: str, button_style: discord.ButtonStyle):
        super().__init__(style=button_style, label=label, emoji=emoji, )

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Confirm = self.view
        view.value = True
        view.stop()


class CancelButton(discord.ui.Button):
    def __init__(self, label: str, emoji: str, button_style: discord.ButtonStyle):
        super().__init__(style=button_style, label=label, emoji=emoji)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Confirm = self.view
        view.value = False
        view.stop()


class Confirm(discord.ui.View):
    def __init__(self, buttons: typing.Tuple[typing.Tuple[str]], timeout: int = 30):
        super().__init__(timeout=timeout)
        self.message = None
        self.value = None
        self.ctx: CustomContext = None
        self.add_item(ConfirmButton(emoji=buttons[0][0],
                                    label=buttons[0][1],
                                    button_style=(
                                            buttons[0][2] or discord.ButtonStyle.green
                                    )))
        self.add_item(CancelButton(emoji=buttons[1][0],
                                   label=buttons[1][1],
                                   button_style=(
                                           buttons[1][2] or discord.ButtonStyle.red
                                   )))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user and interaction.user.id in (self.ctx.bot.owner_id, self.ctx.author.id):
            return True
        messages = [
            "Oh no you can't do that! This belongs to **{user}**",
            'This is **{user}**\'s confirmation, sorry! 💖',
            '😒 Does this look yours? **No**. This is **{user}**\'s confirmation button',
            '<a:stopit:891139227327295519>',
            'HEYYYY!!!!! this is **{user}**\'s menu.',
            'Sorry but you can\'t mess with **{user}**\' menu QnQ',
            'No. just no. This is **{user}**\'s menu.',
            '<:blobstop:749111017778184302>' * 3,
            'You don\'t look like {user} do you...',
            '🤨 Thats not yours! Thats **{user}**\'s',
            '🧐 Whomst! you\'re not **{user}**',
            '_out!_ 👋'
        ]
        await interaction.response.send_message(random.choice(messages).format(user=self.ctx.author.display_name),
                                                ephemeral=True)

        return False

class CustomContext(commands.Context):

    @staticmethod
    def tick(opt: bool, text: str = None) -> str:
        ticks = {
            True: '<:greenTick:596576670815879169>',
            False: '<:redTick:596576672149667840>',
            None: '<:greyTick:860644729933791283>',
        }
        emoji = ticks.get(opt, "<:redTick:596576672149667840>")
        if text:
            return f"{emoji} {text}"
        return emoji

    @staticmethod
    def default_tick(opt: bool, text: str = None) -> str:
        ticks = {
            True: '✅',
            False: '❌',
            None: '➖',
        }
        emoji = ticks.get(opt, "❌")
        if text:
            return f"{emoji} {text}"
        return emoji

    @staticmethod
    def square_tick(opt: bool, text: str = None) -> str:
        ticks = {
            True: '🟩',
            False: '🟥',
            None: '⬛',
        }
        emoji = ticks.get(opt, "🟥")
        if text:
            return f"{emoji} {text}"
        return emoji

    @staticmethod
    def dc_toggle(opt: bool, text: str = None) -> str:
        ticks = {
            True: '<:DiscordON:882991627541565461>',
            False: '<:DiscordOFF:882991627994542080>',
            None: '<:DiscordNONE:882991627994546237>',
        }
        emoji = ticks.get(opt, "<:DiscordOFF:882991627994542080>")
        if text:
            return f"{emoji} {text}"
        return emoji

    @staticmethod
    def toggle(opt: bool, text: str = None) -> str:
        ticks = {
            True: '<:toggle_on:857842924729270282>',
            False: '<:toggle_off:857842924544065536>',
            None: '<:toggle_off:857842924544065536>',
        }
        emoji = ticks.get(opt, "<:toggle_off:857842924544065536>")
        if text:
            return f"{emoji} {text}"
        return emoji
    
    # async def send(self, content=None, **kwargs):
    # tip = random.choice(['your tips here'])
    # if random.randint(1, 100) == 1:
    #     content = f"{tip}\n\n{str(content) if content else ''}"
    #     return await super().send(content, **kwargs)
    # return await super().send(content, **kwargs)

    async def send(self, content: str = None, embed: discord.Embed = None,
                   reply: bool = True, footer: bool = True,
                   reference: typing.Union[discord.Message, discord.MessageReference] = None, **kwargs):

        reference = (reference or self.message.reference or self.message) if reply is True else reference

        if embed and footer is True:
            if not embed.footer:
                embed.set_footer(text=f"Requested by {self.author}",
                                 icon_url=self.author.display_avatar.url)

        if embed:
            colors = [0x910023, 0xA523FF]
            color = random.choice(colors)
            
            embed.timestamp = discord.utils.utcnow()
            embed.color = color
            
        if content is None:
            number = random.randint(0, 15)
            if number == 1:
                content = "Support **Stealth Bot** by voting: <https://top.gg/bot/760179628122964008>"
                
        if content is not None:
            number = random.randint(0, 15)
            if number == 1:
                content = f"{content}\nSupport **Stealth Bot** by voting: <https://top.gg/bot/760179628122964008>"

        try:
            return await super().send(content=content, embed=embed, reference=reference, **kwargs)
        except discord.HTTPException:
            return await super().send(content=content, embed=embed, reference=None, **kwargs)
        
    async def confirm(self, message: str = 'Do you want to confirm?',
                      buttons: typing.Tuple[typing.Union[discord.PartialEmoji, str],
                                            str, discord.ButtonStyle] = None, timeout: int = 30,
                      delete_after_confirm: bool = False, delete_after_timeout: bool = False,
                      delete_after_cancel: bool = None):
        delete_after_cancel = delete_after_cancel if delete_after_cancel is not None else delete_after_confirm
        view = Confirm(buttons=buttons or (
            (None, 'Confirm', discord.ButtonStyle.green),
            (None, 'Cancel', discord.ButtonStyle.red)
        ), timeout=timeout)
        view.ctx = self
        message = await self.send(message, view=view)
        await view.wait()
        if view.value is None:
            try:
                (await message.edit(view=None)) if \
                    delete_after_timeout is False else (await message.delete())
            except (discord.Forbidden, discord.HTTPException):
                pass
            return False
        elif view.value:
            try:
                (await message.edit(view=None)) if \
                    delete_after_confirm is False else (await message.delete())
            except (discord.Forbidden, discord.HTTPException):
                pass
            return True
        else:
            try:
                (await message.edit(view=None)) if \
                    delete_after_cancel is False else (await message.delete())
            except (discord.Forbidden, discord.HTTPException):
                pass
            return False

class StealthBot(commands.AutoShardedBot):
    PRE: tuple = ('sb!',)
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=self.get_pre, *args, **kwargs)

    async def get_pre(self, bot, message: discord.Message, raw_prefix: Optional[bool] = False) -> List[str]:
        if not message:
            return commands.when_mentioned_or(*self.PRE)(bot, message) if not raw_prefix else self.PRE
        if not message.guild:
            return commands.when_mentioned_or(*self.PRE)(bot, message) if not raw_prefix else self.PRE
        try:
            prefix = self.prefixes[message.guild.id]
        except KeyError:
            prefix = (await self.db.fetchval('SELECT prefix FROM guilds WHERE guild_id = $1',
                                             message.guild.id)) or self.PRE
            prefix = prefix if prefix[0] else self.PRE

            self.prefixes[message.guild.id] = prefix

        if await bot.is_owner(message.author) and bot.no_prefix is True:
            return commands.when_mentioned_or(*prefix, "")(bot, message) if not raw_prefix else prefix
        return commands.when_mentioned_or(*prefix)(bot, message) if not raw_prefix else prefix
    
    async def get_context(self, message, *, cls=CustomContext):
        return await super().get_context(message, cls=cls)

client = StealthBot(
    intents=discord.Intents.all(),
    activity=activity,
    status=status,
    case_insensitive=True,
    help_command=None,
    enable_debug_events=True,
    strip_after_prefix=True) # Initializes the client object

client.tracker = DiscordUtils.InviteTracker(client) # Initializes the tracker object
client.owner_ids = [564890536947875868, 555818548291829792] # 349373972103561218 (LeoCx1000) # 555818548291829792 (Vicente0670)
client.launch_time = discord.utils.utcnow()
client.no_prefix = False
client.maintenance = False
client.invite_url = "https://discord.com/api/oauth2/authorize?client_id=760179628122964008&permissions=8&scope=bot"
client.top_gg = "https://top.gg/bot/760179628122964008"
client.bots_gg = "https://discord.bots.gg/bots/760179628122964008"
client.github = "https://github.com/Ender2K89/Stealth-Bot"
#client.allowed_mentions = discord.AllowedMentions(replied_user=False)
client.allowed_mentions = discord.AllowedMentions.none()
client.session = aiohttp.ClientSession()
client.blacklist = {}
client.prefixes = {}
client.brain_cells = 0
client._BotBase__cogs = commands.core._CaseInsensitiveDict()
client.user_id = int('760179628122964008')
client.afk_users = {}
client.token = "haha no"
client.reddit = asyncpraw.Reddit(client_id=yaml_data['ASYNC_PRAW_CLIENT_ID'],
                                client_secret=yaml_data['ASYNC_PRAW_CLIENT_SECRET'],
                                user_agent=yaml_data['ASYNC_PRAW_USER_AGENT'],
                                username=yaml_data['ASYNC_PRAW_USERNAME'],
                                password=yaml_data['ASYNC_PRAW_PASSWORD'])

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "true"

	# Functions and stuff

async def create_db_pool():
    credentials = {"user": "postgres",
                   "password": "1211",
                   "database": "stealthdb",
                   "host": "localhost"}

    client.db = await asyncpg.create_pool(**credentials)
    print("connected to PostgreSQL")

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
    change_vc.start() # Starts the task called "change_vc"

    print("started task: change_vc") # Prints "Started task: change_vc"
    print('-------------================----------------') # Prints some lines to make it look better
    print(f"connected to bot: {client.user.name}") # Prints "Connected to the bot {Name of the bot}"
    print(f"bot ID: {client.user.id}") # Prints "Bot ID {ID of the bot}"
    print('-------------================----------------') # Prints some lines to make it look better

    channel = client.get_channel(883658687867158529) # Get the channel called "bot_logs" (883658687867158529) and store it as the variable "channel"

    embed = discord.Embed(title="Bot started", color=0x2F3136) # Creates a embed with the title being "Bot started" and the color being 0x2F3136

    await channel.send(embed=embed) # Sends the embed in the channel

    await client.tracker.cache_invites() # Caches the invites

    print("tracker has been loaded")

# ---------------------------------------------------------------------------------------------- #

os.system('clear')

client.load_extension('jishaku')
print("jishaku has been loaded")


for filename in os.listdir('./cogs'): # For every file in the folder called "cogs"
    if filename.endswith('.py'): # If the file ends with .py
        client.load_extension(f'cogs.{filename[:-3]}') # Load the file as a extension/cog
        print(f'{filename[:-3]}.py has been loaded')
print('-------------================----------------')

# ---------------------------------------------------------------------------------------------- #

async def run_once_when_ready():
    await client.wait_until_ready()
    values = await client.db.fetch("SELECT user_id, is_blacklisted FROM blacklist")

    for value in values:
        client.blacklist[value['user_id']] = (value['is_blacklisted'] or False)
    print("blacklist system has been loaded")

    values = await client.db.fetch("SELECT guild_id, prefix FROM guilds")

    for value in values:
        if value['prefix']:
            client.prefixes[value['guild_id']] = ((value['prefix'] if value['prefix'][0] else PRE) or PRE)

    for guild in client.guilds:
        if not guild.unavailable:
            try:
                client.prefixes[guild.id]
            except KeyError:
                client.prefixes[guild.id] = PRE
                
@client.check
def maintenance(ctx):
    if client.maintenance is False:
        return True
    else:
        raise errors.BotMaintenance

@client.check
def blacklist(ctx):
    try:
        is_blacklisted = client.blacklist[ctx.author.id]
    except KeyError:
        is_blacklisted = False
    if ctx.author.id == client.owner_id:
        is_blacklisted = False

    if is_blacklisted is False:
        return True
    else:
        raise errors.AuthorBlacklisted

@client.event
async def on_invite_create(invite):
    if invite.guild.id == 799330949686231050 or invite.guild.id == 882341595528175686:
        await tracker.update_invite_cache(invite)

@client.event
async def on_invite_delete(invite):
    if invite.guild.id == 799330949686231050 or invite.guild.id == 882341595528175686:
        await tracker.remove_invite_cache(invite)


# @client.event
# async def on_message(message):
#     if message.content in [f'<@!{client.user.id}>', f'<@{client.user.id}>']:
#         await message.reply(f"fuck off", mention_author=False)
#     if not message.guild: # If the message wasn't sent in a guild then:
#         return await client.process_commands(message) # Return and process the command.
#     if message.guild.id in moderated_servers:
#         if len(message.content) >  500: # If the length of the message is over 500 then:
#             await message.delete() # Deletes the message
#             warnMessage = f"Hey {message.author.mention}! Your message was over 500 characters so I had to delete it!\n*If you think this was a mistake then please contact Ender2K89 (The owner of this bot & server)*" # String that tells the author to not send messages over 500 messages
#             await message.channel.send(warnMessage, delete_after=5.0) # Sends the warnMessage and deletes it after 5 seconds
#         if message.channel.id in social_category or message.channel.id in fun_stuff_category or message.channel.id in no_mic_channel: # If the message was sent in the social, fun stuff category or the no mic channel then:
#             #url_regex = re.compile(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*')
#             #url_regex = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
#             invite_regex = re.compile(r"<?(https?:\/\/)?(www\.)?(discord\.gg|discordapp\.com\/invite)\b([-a-zA-Z0-9/]*)>?")
#             link_perms_role = discord.utils.get(message.guild.roles, name="Link Perms")
#
#             if link_perms_role in message.author.roles:
#                 await client.process_commands(message) # Processes commands
#                 return # Return (ignore)
#             else:
#                 if invite_regex.search(message.content):
#                     await message.delete() # Deletes the message
#                     warnMessage = f"Hey {message.author.mention}! Sending discord invites is not allowed!" # String that tells the author to stop sending discord invites
#                     await message.channel.send(warnMessage, delete_after=5.0) # Sends the warnMessage and deletes it after 5 seconds
#                 else: # If it didn't match then:
#                     pass # I don't know what to put
#     await client.process_commands(message) # Processes commands

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
client.loop.create_task(run_once_when_ready())
client.run(yaml_data['TOKEN'], reconnect=True) # Runs the bot with the token being the variable "TOKEN"
