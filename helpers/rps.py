import asyncio
import discord
from discord import Interaction

class ObjectSelector(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Rock", description="Rock beats Scissors", emoji=":rock:"),
            discord.SelectOption(label="Paper", description="Paper beats Rock", emoji=":newspaper:"),
            discord.SelectOption(label="Scissors", description="Scissors beats Paper", emoji=":scissors:")
        ]
        
        super().__init__(placeholder="Select your object", min_values=1, max_values=1, options=options)

    async def callback(self, interaction : discord.Interaction):
        assert self.view is not None
        view: RockPaperScissors = self.view
        view.responses[interaction.user.id] = self.values[0]

        embed = view.message.embeds[0].copy()
        embed.description = f"{view.ctx.tick(view.player1.id in view.responses)} {view.player1.display_name}\n{view.ctx.tick(view.player2.id in view.responses)} {view.player2.display_name}"

        await view.message.edit(embed=embed)

        if len(view.responses) == 2:
            response = view.check_winner()
            embed.description = f"""
<:greenTick:596576670815879169> {view.player1.display_name} chose {view.responses[view.player1.id]}
<:greenTick:596576670815879169> {view.player2.display_name} chose {view.responses[view.player2.id]}

{response}
            """

            for item in view.children:
                if isinstance(item, discord.ui.Select):
                    item.placeholder = "The game has ended!"
                item.disabled = True

            await asyncio.sleep(1)
            await view.message.edit(embed=embed, view=view)


class RockPaperScissors(discord.ui.View):

    def __init__(self, ctx, player1 : discord.Member, player2 : discord.Member):
        super().__init__()
        self.message : discord.Message = None
        self.ctx : commands.Context = ctx
        self.player1: discord.Member = player1
        self.player2: discord.Member = player2
        self.responses = {}
        self.add_item(ObjectSelector())

    async def interaction_check(self, interaction : Interaction):
        if not interaction.user or interaction.user.id not in (self.player1.id, self.player2.id):
            await interaction.response.send_message("You aren't a part of this game!", ephemeral=True)
            return False
        
        if interaction.user.id in self.responses:
            await interaction.response.send_message(f"You've already selected {self.responses[interaction.user.id]}, it's too late to change it now!", ephemeral=True)
            return False
        
        return True

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Select):
                item.placeholder = "Timed out! Please try again."
            item.disabled = True
        await self.message.edit(view=self)

    def check_winner(self):
        mapping = {
            'Rock': 0,
            'Paper': 1,
            'Scissors': 2
        }
        win_1 = f":tada: __**{self.player1.display_name} WON!!!**__ :tada:\n{self.responses[self.player1.id]} beats {self.responses[self.player2.id]}"
        win_2 = f":tada: __**{self.player2.display_name} WON!!!**__ :tada:\n{self.responses[self.player2.id]} beats {self.responses[self.player1.id]}"
        tie = f":necktie: It's a tie!"

        if self.responses[self.player1.id] == self.responses[self.player2.id]:
            return tie
        
        elif (mapping[self.responses[self.player1.id]] + 1) % 3 == mapping[self.responses[self.player2.id]]:
            return win_2
        
        else:
            return win_1