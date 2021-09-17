import discord
import datetime
from discord.ext import commands
import helpers
from difflib import get_close_matches
import traceback
from cogs import music as music_cog
import errors

def setup(client):
    client.add_cog(errorhandler(client))

class errorhandler(commands.Cog):
    def __init__(self, client):
        self.hidden = True
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx : commands.Context, error : commands.CommandError):
        prefix = ctx.clean_prefix

        error = getattr(error, "original", error)

        ignored = (
            music_cog.NoPlayer,
            music_cog.FullVoiceChannel,
            music_cog.NotAuthorized,
            music_cog.IncorrectChannelError,
            music_cog.AlreadyConnectedToChannel,
            music_cog.NoVoiceChannel,
            music_cog.QueueIsEmpty,
            music_cog.NoCurrentTrack,
            music_cog.PlayerIsAlreadyPaused,
            music_cog.PlayerIsNotPaused,
            music_cog.NoMoreTracks,
            music_cog.InvalidTimeString,
            music_cog.NoPerms,
            music_cog.NoConnection,
            music_cog.AfkChannel,
            music_cog.SkipInLoopMode,
            music_cog.InvalidTrack,
            music_cog.InvalidPosition,
            music_cog.InvalidVolume,
            music_cog.OutOfTrack,
            music_cog.NegativeSeek
        )
        
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.CommandNotFound):
            if ctx.author.id == 564890536947875868 and self.client.no_prefix is True:
                return


            message = f"I couldn't find that command."
            command_names = [str(x) for x in ctx.bot.commands]
            matches = get_close_matches(ctx.invoked_with, command_names)
            if matches:
                matches = "\n".join(matches)
                message = f"I couldn't find that command. Did you mean...\n{matches}"

        elif isinstance(error, errors.AuthorBlacklisted):
            message = f"It appears that you're blacklisted from this bot. Contact Ender2K89#9999 if you think this is a mistake."

        elif isinstance(error, helpers.NotSH):
            message = f"You can only use this command in `Stealth Hangout`!\ndiscord.gg/ktkXwmD2kF"

        elif isinstance(error, helpers.NotCSMP):
            message = f"You can only use this command in `ClassicSMP`!\nhttps://discord.gg/afBDa2Kqc9"

        elif isinstance(error, errors.TooLongPrefix):
            message = f"Prefixes can only be up to 50 characters!"

        elif isinstance(error, errors.TooManyPrefixes):
            message = f"You can only have 20 prefixes!"

        elif isinstance(error, errors.PrefixAlreadyExists):
            message = f"That's already one of my prefixes!"

        elif isinstance(error, errors.PrefixDoesntExist):
            message = f"That's not one of my prefixes!"

        elif isinstance(error, errors.KillYourself):
            message = f"I couldn't find that command. Did you mean...\nkill {ctx.author.mention}"

        elif isinstance(error, errors.CommandDoesntExist):
            message = f"I couldn't find that category/command."

        elif isinstance(error, helpers.Blacklisted):
            message = f"It appears that you're blacklisted from this bot. Contact Ender2K89#9999 if you think this is a mistake."

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

            embed = discord.Embed(title=message, color=0x2F3136)
            embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")

            return await ctx.reply(embed=embed)

        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            missing=f"{str(error.param).split(':')[0]}"
            command = f"{ctx.prefix}{ctx.command} {ctx.command.signature}"
            separator = (' ' * (len(command.split(missing)[0])-1))
            indicator = ('^' * (len(missing)+2))
            message = f"```{command}\n{separator}{indicator}\n{missing} is a required argument that is missing.```"
            return await ctx.send(f"""```{command}\n{separator}{indicator}\n{missing} is a required argument that is missing.```""")

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
            message = f"An unexpected error occurred.\nI've reported it to the devs."

            traceback_string = "".join(traceback.format_exception(etype=None, value=error, tb=error.__traceback__))

            channel = self.client.get_channel(886572124477730848)

            await channel.send(f"""
Author: {ctx.author} **|** {ctx.author.id} **|** {ctx.author.mention}
Channel: {ctx.channel} **|** {ctx.channel.id} **|** {ctx.channel.mention}
Server: {ctx.guild} **|** {ctx.guild.id}

Traceback:
```
{traceback_string}
```
            """)
        embed = discord.Embed(description=message, color=0x2F3136)

        await ctx.reply(embed=embed)
