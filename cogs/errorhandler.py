import discord
import datetime
from discord.ext import commands
import helpers
import traceback

class errorhandler(commands.Cog):
    def __init__(self, client):
        self.hidden = True
        self.client = client


    @commands.Cog.listener()
    async def on_command_error(self, ctx : commands.Context, error : commands.CommandError):
        prefix = await self.client.db.fetchval('SELECT prefix FROM guilds WHERE guild_id = $1', ctx.guild.id)
        prefix = prefix or 'sb!'

        if isinstance(error, commands.CommandNotFound):
            if ctx.author.id == 564890536947875868 and ctx.bot.no_prefix is True: return
            message = f"I couldn't find that command, do `{prefix}help` to see a list of all commands."

        elif isinstance(error, helpers.NotSH):
            message = f"You can only use this command in `Stealth Hangout`!\ndiscord.gg/ktkXwmD2kF"

        elif isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."

        elif isinstance(error, discord.Forbidden):
            message = f"""
I don't have the permissions to do that.
This might be due to me missing permissions in the current channel or server.
This might also be a issue with role hierarchy, try to change my permissions for this server.
Note: I can't edit the owner of the server
            """

        elif isinstance(error, discord.HTTPException):
            message = "An unexpected HTTP error occurred.\nPlease notify Ender2K89#9999 about this issue with a screenshot of what you're trying to do."

        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command."

        elif isinstance(error, commands.NotOwner):
            message = "Only the owner of this bot can run this command."

        elif isinstance(error, commands.TooManyArguments):
            message = "It appears that you've provided too many arguments, please try again with fewer arguments."

        elif isinstance(error, commands.MemberNotFound):
            message = "I couldn't find that member."

        elif isinstance(error, commands.MessageNotFound):
            message = "I couldn't find that message."

        elif isinstance(error, commands.GuildNotFound):
            message = "I couldn't find that guild."

        elif isinstance(error, commands.ChannelNotFound):
            message = "I couldn't find that channel."

        elif isinstance(error, commands.UserNotFound):
            message = "I couldn't find that user."

        elif isinstance(error, commands.ChannelNotReadable):
            message = "I cannot read that channel."

        elif isinstance(error, commands.NSFWChannelRequired):
            message = "This command can only be used in a NSFW channel."

        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            missing=f"{str(error.param).split(':')[0]}"
            command = f"{ctx.prefix}{ctx.command} {ctx.command.signature}"
            separator = (' ' * (len(command.split(missing)[0])-1))
            indicator = ('^' * (len(missing)+2))
            print(f"`{separator}`  `{indicator}`")
            print(error.param)
            print()
            await ctx.send(f"""```{command}\n{separator}{indicator}\n{missing} is a required argument that is missing.```""")
            return

        elif isinstance(error, commands.RoleNotFound):
            message = "I couldn't find that role."

        elif isinstance(error, commands.MissingRole):
            message = "You're missing a role that's required to run this command."

        elif isinstance(error, commands.BotMissingPermissions):
            message = "I don't have the permissions to do that."

        elif isinstance(error, commands.ExtensionFailed):
            message = "That extension/cog failed."

        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            message = "That extension/cog is already loaded."

        elif isinstance(error, commands.ExtensionNotFound):
            message = "I couldn't find that extension/cog."

        else:
            message = f"An unexpected error occurred.\n{error}"

        # errormessage = f"{error}"
        # embed = discord.Embed(description=message, timestamp=discord.utils.utcnow(), color=0x2F3136)
        await ctx.reply(message)
        # await ctx.send(error)


def setup(client):
    client.add_cog(errorhandler(client))
