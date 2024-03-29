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
from helpers.ttt import LookingToPlay, TicTacToe

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
                return f":necktie: It's a tie!"
            elif authorAnswer == "rock" and botAnswer == "paper":
                return f":tada: __**{botName} WON!!!**__ :tada:"
            elif authorAnswer == "rock" and botAnswer == "scissors":
                return f":tada: __**{authorName} WON!!!**__ :tada:"

            elif authorAnswer == "paper" and botAnswer == "rock":
                return f":tada: __**{authorName} WON!!!**__ :tada:"
            elif authorAnswer == "paper" and botAnswer == "paper":
                return f":necktie:  It's a tie!"
            elif authorAnswer == "paper" and botAnswer == "scissors":
                return f":tada: __**{botName} WON!!!**__ :tada:"

            elif authorAnswer == "scissors" and botAnswer == "rock":
                return f":tada: __**{botName} WON!!!**__ :tada:"
            elif authorAnswer == "scissors" and botAnswer == "paper":
                return f":tada: __**{authorName} WON!!!**__ :tada:"
            elif authorAnswer == "scissors" and botAnswer == "scissors":
                return f":necktie: It's a tie!"

            else:
                return f"I have no idea who won."


        def check(m):
            return m.content.lower() in validAnswers and m.channel.id == ctx.channel.id and m.author.id == ctx.author.id
        
        await ctx.send("Pick one! `rock`, `paper`, `scissors`")

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
            
            if result == f":tada: __**{ctx.author.name} WON!!!**__ :tada:":
                shortText = f"{str(authorAnswer).title()} beats {str(botAnswer).title()}"
                longText = f"{str(authorAnswer).title()} beats {str(botAnswer).title()} meaning {ctx.author.name} won."
                
            elif result == f":tada: __**Stealth Bot WON!!!**__ :tada:":
                shortText = f"{str(botAnswer).title()} beats {str(authorAnswer).title()}"
                longText = f"{str(botAnswer).title()} beats {str(authorAnswer).title()} meaning Stealth Bot won."
                
            else:
                shortText = f":necktie: It's a tie!"
                longText = f"{str(botAnswer).title()} doesn't beat {str(authorAnswer).title()} and {str(authorAnswer).title()} doesn't beat {str(botAnswer).title()} meaning it's a tie."

            embed = discord.Embed(title=result, description=f"""
{ctx.author.name}'s answer: {str(authorAnswer).title()}
Stealth Bot's answer: {str(botAnswer).title()}
[Hover over this text to see why]({msg.jump_url} '{longText}')
                                  """, timestamp=discord.utils.utcnow())
            embed.set_footer(text=shortText)

            await ctx.reply(embed=embed)
            
    @commands.command(help="Starts a Tic-Tac-Toe game", aliases=['ttt', 'tic'])
    async def tictactoe(self, ctx):
        embed = discord.Embed(description=f"🔎 {ctx.author.name} is looking to play Tic-Tac-Toe!")
        
        player1 = ctx.author
        view = LookingToPlay(timeout=120)
        view.ctx = ctx
        view.message = await ctx.send(embed=embed, view=view)
        await view.wait()
        player2 = view.value
        
        if player2:
            starter = random.choice([player1, player2])
            ttt = TicTacToe(ctx, player1, player2, starter=starter)
            ttt.message = await view.message.edit(content=f'#️⃣ {starter.name} goes first', view=ttt, embed=None)
            await ttt.wait()