from aiohttp import helpers
import discord
import random
import helpers.helpers as helpers
import asyncio
import re
import io
import datetime
import aiohttp
import time
import pyfiglet
from discord.ext import commands, menus
from discord.ext.menus.views import ViewMenuPages
from discord.ext.commands.cooldowns import BucketType

def setup(client):
    client.add_cog(Games(client))

class Games(commands.Cog):
    ":video_game: | Commands used to play games when you're bored!" 
    def __init__(self, client):
        self.client = client

    @commands.command(
        help="RPG.",
        aliases=['fight', 'r'])
    async def rpg(self, ctx):
        validAnswers1 = ['yes', 'no']
        validAnswers2 = ['fight', 'stop']
        authorName = ctx.author.name
        pensiveName = "pensive"
        authorHP = 100
        pensiveHP = 100
        pensiveMinimumDamage = 0
        pensiveMaximumDamage = 10
        authorMinimumDamage = 0
        authorMaximumDamage = 10
        
        def hp(argument):
            if argument == 0:
                return "▒▒▒▒▒▒▒▒▒▒ 💔"
            if argument == 10:
                return "█▒▒▒▒▒▒▒▒▒ ❤️"
            elif argument == 20:
                return "██▒▒▒▒▒▒▒▒ ❤️"
            elif argument == 30:
                return "███▒▒▒▒▒▒▒ ❤️"
            elif argument == 40:
                return "████▒▒▒▒▒▒ ❤️"
            elif argument == 50:
                return "█████▒▒▒▒▒ ❤️"
            elif argument == 60:
                return "██████▒▒▒▒ ❤️"
            elif argument == 70:
                return "███████▒▒▒ ❤️"
            elif argument == 80:
                return "████████▒▒ ❤️"
            elif argument == 90:
                return "█████████▒ ❤️"
            elif argument == 100:
                return "██████████ ❤️"
            else:
                return "▒▒▒▒▒▒▒▒▒▒ 💔"

        def check1(m):
            return m.content.lower() in validAnswers1 and m.channel.id == ctx.channel.id and m.author.id == ctx.author.id
        
        def check2(m):
            return m.content.lower() in validAnswers2 and m.channel.id == ctx.channel.id and m.author.id == ctx.author.id
            
        await ctx.send("Do you want to turn hard-code mode on? `yes/no`")
        
        try:
            msg = await self.client.wait_for(event='message', check=check1, timeout=15)
            
        except asyncio.TimeoutError:
            return await ctx.send("It's been over 15 seconds, please try again by doing `-rpg`.")
        
        else:
            
            if msg.content == "yes":
                pensiveMinimumDamage = 4
                pensiveMaximumDamage = 20
                authorMinimumDamage = 2
                authorMaximumDamage = 6
        
            await ctx.send("What do you want to do? `fight/stop`") # <------ this wont work cause its not inside the if statement
            
            try:
                msg = await self.client.wait_for(event='message', check=check2, timeout=15)
                
            except asyncio.TimeoutError:
                return await ctx.send("It's been over 15 seconds, please try again by doing `-rpg`.")
            
            else:
                if msg.content.lower() == "stop":
                    return await ctx.send("Okay, stopped RPG.")
                
                number1 = random.randint(authorMinimumDamage, authorMaximumDamage)
                number = number1 * 10
                pensiveHP = pensiveHP - number
                
                if pensiveHP < 10:
                    return await ctx.send(f"__**🎉 {authorName} WON!!! 🎉**__\nYou did `{number}` damage to {pensiveName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                
                await ctx.send(f"You did `{number}` damage to {pensiveName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                
                number1 = random.randint(pensiveMinimumDamage, pensiveMaximumDamage)
                number = number1 * 10
                authorHP = authorHP - number
                
                await asyncio.sleep(2)

                if authorHP < 10:
                    return await ctx.send(f"__**🎉 {pensiveName} WON!!! 🎉**__\n{pensiveName} did `{number}` damage to {authorName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")

                await ctx.send(f"{pensiveName} did `{number}` damage to {authorName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                
                message = await ctx.send("What do you want to do? `fight/stop`")

                try:
                    msg = await self.client.wait_for(event='message', check=check2, timeout=15)
                    
                except asyncio.TimeoutError:
                    return await ctx.send("It's been over 15 seconds, please try again by doing `-rpg`")
                
                else:
                    if msg.content.lower() == "stop":
                        return await ctx.send("Okay, stopped RPG.")
                    
                    number1 = random.randint(authorMinimumDamage, authorMaximumDamage)
                    number = number1 * 10
                    pensiveHP = pensiveHP - number
                    
                    if pensiveHP < 10:
                        return await ctx.send(f"__**🎉 {authorName} WON!!! 🎉**__\nYou did `{number}` damage to {pensiveName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                    
                    await ctx.send(f"You did `{number}` damage to {pensiveName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                    
                    number1 = random.randint(pensiveMinimumDamage, pensiveMaximumDamage)
                    number = number1 * 10
                    authorHP = authorHP - number
                    
                    await asyncio.sleep(2)

                    if authorHP < 10:
                        return await ctx.send(f"__**🎉 {pensiveName} WON!!! 🎉**__\n{pensiveName} did `{number}` damage to {authorName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")

                    await ctx.send(f"{pensiveName} did `{number}` damage to {authorName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                    
                    message = await ctx.send("What do you want to do? `fight/stop`")
                    
                    try:
                        msg = await self.client.wait_for(event='message', check=check2, timeout=15)
                        
                    except asyncio.TimeoutError:
                        return await ctx.send("It's been over 15 seconds, please try again by doing `-rpg`")
                    
                    else:
                        if msg.content.lower() == "stop":
                            return await ctx.send("Okay, stopped RPG.")
                        
                        number1 = random.randint(authorMinimumDamage, authorMaximumDamage)
                        number = number1 * 10
                        pensiveHP = pensiveHP - number
                        
                        if pensiveHP < 10:
                            return await ctx.send(f"__**🎉 {authorName} WON!!! 🎉**__\nYou did `{number}` damage to {pensiveName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                        
                        await ctx.send(f"You did `{number}` damage to {pensiveName}!\n{authorName}'s HP: {hp(authorHP)}\n{pensiveName}'s HP: {hp(pensiveHP)}")
                        
    @commands.command(
        help="Plays rock, paper, scissors with you",
        aliases=['rps', 'rock_paper_scissors'])
    async def rockpaperscissors(self, ctx):
        validAnswers = ['rock', 'paper', 'scissors', 'win']
        botAnswers = ['rock', 'paper', 'scissors']

        def rockPaperScissors(authorName, botName, authorAnswer, botAnswer):
            if authorAnswer == "rock" and botAnswer == "rock":
                return f":tada: It's a tie! :tada:"
            elif authorAnswer == "rock" and botAnswer == "paper":
                return f":tada: {botName} won! :tada:"
            elif authorAnswer == "rock" and botAnswer == "scissors":
                return f":tada: {authorName} won! :tada:"

            elif authorAnswer == "paper" and botAnswer == "rock":
                return f":tada: {authorName} won! :tada:"
            elif authorAnswer == "paper" and botAnswer == "paper":
                return f":tada: It's a tie! :tada:"
            elif authorAnswer == "paper" and botAnswer == "scissors":
                return f":tada: {botName} won! :tada:"

            elif authorAnswer == "scissors" and botAnswer == "rock":
                return f":tada: {botName} won! :tada:"
            elif authorAnswer == "scissors" and botAnswer == "paper":
                return f":tada: {authorName} won! :tada:"
            elif authorAnswer == "scissors" and botAnswer == "scissors":
                return f":tada: It's a tie! :tada:"

            else:
                return f"I have no idea who won."


        def check(m):
            return m.content.lower() in validAnswers and m.channel.id == ctx.channel.id and m.author.id == ctx.author.id
        
        message = await ctx.send("Pick one! `rock`, `paper`, `scissors`")

        try:
            msg = await self.client.wait_for(event='message', check=check, timeout=15)

        except asyncio.TimeoutError:
            return await ctx.send("It's been over 15 seconds, please try again by doing `-rpg`.")

        else:
            
            authorAnswer = msg.content.lower()
            botAnswer = random.choice(botAnswers)
            
            if msg.content.lower() == "win":
                authorAnswer = "rock"
                botAnswer = "scissors"
                
            result = rockPaperScissors(authorName=ctx.author.name, botName="Stealth Bot", authorAnswer=authorAnswer, botAnswer=botAnswer)
            
            if result == f":tada: {ctx.author.name} won! :tada:":
                text = f"{str(authorAnswer).title()} beats {str(botAnswer).title()}"
                
            elif result == f":tada: Stealth Bot won! :tada:":
                text = f"{str(botAnswer).title()} beats {str(authorAnswer).title()}"
                
            else:
                text = f"It's a tie!"

            embed = discord.Embed(title=result, description=f"""
{ctx.author.name}'s answer: {authorAnswer}
Stealth Bot's answer: {botAnswer}
                                  """, timestamp=discord.utils.utcnow())
            embed.set_footer(text=text)

            await ctx.reply(embed=embed)