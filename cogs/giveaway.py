import discord
import datetime
import helpers
import random
from random import choice
from asyncio import TimeoutError, sleep
import discord
import random
from discord.ext import commands

def convert(time):
    pos = ["s","m","h","d"]
    time_dict = {"s": 1,"m": 60,"h": 3600,"d": 24*3600 }
    unit = time[-1]
    if unit not in pos:
        return -1
    try:
        timeVal = int(time[:-1])
    except:
        return -2

    return timeVal*time_dict[unit]

class giveaway(commands.Cog):
    "Commands that are used to reroll/start a giveaway"
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['gstart', 'start_giveaway', 'gcreate'])
    @commands.check_any(commands.has_permissions(manage_guild=True), commands.is_owner())
    @commands.cooldown(1, 60, commands.BucketType.user) # Sets the cooldown to 60 seconds for the user executing the command
    async def giveaway(self, ctx):
        def format_dt(dt, style=None):
            if style is None:
                return f'<t:{int(dt.timestamp())}>'
            return f'<t:{int(dt.timestamp())}:{style}>'

        def format_relative(dt):
            return format_dt(dt, 'R')

        def format_date(dt):
            if dt is None:
                return 'N/A'
            return f'{format_dt(dt, "F")} ({format_relative(dt)})'

        emote = "🎉"

        firstEmbed = discord.Embed(title="Starting Giveaway", description="Answer these 4 questions within 30 seconds", timestamp=discord.utils.utcnow(), color=0x2F3136) # Makes a embed called "firstEmbed"

        await ctx.reply(embed=firstEmbed) # Sends the first embed

        questions = ["What channel should the giveaway be hosted in?", "How long should the giveaway last? (s|m|h|d)", "What's the prize for this giveaway?", "What's the claim time for this giveaway?"] # Stores the questions in a variable called "questions"

        answers = [] # Stores the answers in a variable called "answers"

        def check(m): # Check function
            return m.author == ctx.author and m.channel == ctx.channel

        for lol, question in enumerate(questions):
            questionEmbed = discord.Embed(title=f"Question {lol+1}", description=question, timestamp=discord.utils.utcnow(), color=0x2F3136) # Makes a embed called "questionEmbed"

            await ctx.reply(embed=questionEmbed) # Sends the questionEmbed

            try: # Try:
                message = await self.client.wait_for('message', timeout=30, check=check) # Waits 25 seconds for the author to respond to the question
            except TimeoutError: # If they didn't answer in time then:
                await ctx.reply("You didn't answer the questions in time, please try again by doing `-gstart`.") # Tells the author that they didn't answer in time
                return
            answers.append(message.content)
        try: # Try:
            channel_id = int(answers[0][2:-1]) # Find channel with that ID
        except:
            await ctx.reply(f"You didn't provide a valid channel, please try again by doing `-gstart`.") # Tells the author that the channel was invalid
            return

        channel = self.client.get_channel(channel_id) #
        time = convert(answers[1]) # Converts the answer 2 (How long should the giveaway last? (s|m|h|d)) to a valid time and stores it as the "time" variable
        if time == -1:
            await ctx.reply("You didn't provide a valid time, please try again by doing `-gstart`.\n*Example: 6h") # Tells the author that they didn't provide a valid time
            return
        prize = answers[2] # Stores the answer 3 (What's the prize for this giveaway?) as the variable prize

        await ctx.reply(f"The giveaway will be hosted in {channel.mention} and will last {answers[1]}")

        embed = discord.Embed(title=f"{emote} Giveaway Started {emote}", description=f"React with {emote} to enter the giveaway!", timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.add_field(name="Prize", value=prize, inline=True)
        embed.add_field(name="Ends in", value=f"{answers[1]} from now", inline=True)
        embed.add_field(name="Hosted by", value=ctx.author.mention, inline=True)
        embed.add_field(name="Claim time", value=f"{answers[3]}", inline=True)
        embed.set_footer(text=f"1 winner | Giveway ends {answers[1]} from now")

        joinMessage = await channel.send(embed=embed)

        await joinMessage.add_reaction(emote) # Adds the variable "emote" to the joinMessage embed
        await sleep(time)
        fetchedJoinMessage = await channel.fetch_message(joinMessage.id)

        users = await fetchedJoinMessage.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))
        if len(users) <= 0: # If the amount of users is less than 0 then:
            emptyEmbed = discord.Embed(title=f"🎉 Giveaway Ended 🎉", color=0x2F3136)
            emptyEmbed.add_field(name="Prize", value=prize, inline=True)
            emptyEmbed.add_field(name="Hosted by", value=ctx.author.mention, inline=True)
            emptyEmbed.set_footer(text="No one entered the giveaway.")

            await fetchedJoinMessage.edit(embed=emptyEmbed)

            return
        if len(users) > 0: # If the amount of users is more than 1 then:
            winner = choice(users) # Winner = 1 of the users

            winnerEmbed = discord.Embed(title=f"🎉 Giveaway Ended 🎉", color=0x2F3136)
            winnerEmbed.add_field(name="Prize", value=prize, inline=True)
            winnerEmbed.add_field(name="Winner", value=winner.mention, inline=True)
            winnerEmbed.add_field(name="Hosted by", value=ctx.author.mention, inline=True)
            winnerEmbed.add_field(name="Claim time", value=f"{answers[3]}")
            winnerEmbed.set_footer(text=f"Winner: {winner}")

            await fetchedJoinMessage.edit(embed=winnerEmbed)
            await channel.send(f"Congratulations! {winner.mention} won `{prize}`! Contact {ctx.author.mention} for your prize!")
            return

	# reroll command

    @commands.command(aliases=['rerollgiveaway', 'greroll', 'giveawayreroll'])
    @commands.check_any(commands.has_permissions(manage_guild=True), commands.is_owner())
    @commands.cooldown(1, 5, commands.BucketType.user) # Sets the cooldown to 5 seconds for the user executing the command
    async def reroll(self, ctx, channel : discord.TextChannel, message : int):
        try: # Tries to:
            msg = await channel.fetch_message(message) # Fethces the message that the user entered
        except: # Except:
            await ctx.reply(f"I couldn't find that message ID.") # Tells the user that the ID of the message was wrong
            return

        users = await msg.reactions[0].users().flatten() # Gets all the people that reacted to the giveaway message
        users.pop(users.index(self.client.user)) # Excludes the bot

        winner = random.choice(users) # Chooses a random person from the users

        await channel.send(f"Congratulations! The new winner is {winner.mention}! Contact {ctx.author.mention} for your prize!")


def setup(client):
    client.add_cog(giveaway(client))
