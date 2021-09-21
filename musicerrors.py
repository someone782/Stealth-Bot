import discord
from discord.ext import commands

__all__ = (
    'NoPlayer',
    'FullVoiceChannel',
    'NotAuthorized',
    'IncorrectChannelError',
    'IncorrectTextChannelError',
    'AlreadyConnectedToChannel',
    'NoVoiceChannel',
    'QueueIsEmpty',
    'NoCurrentTrack',
    'NoConnection',
    'PlayerIsAlreadyPaused',
    'PlayerIsNotPaused',
    'NoMoreTracks',
    'InvalidTimeString',
    'NoPerms',
    'AfkChannel',
    # 'SkipInLoopMode',
    'InvalidTrack',
    'InvalidPosition',
    'InvalidVolume',
    'OutOfTrack',
    'NegativeSeek',
    'NotAuthorized',

)
class BotError(commands.CommandError):
    def __init__(self, e) -> None:
        self.custom = True
        self.embed = discord.Embed(title='Error occured',color = 0xe74c3c,description = e)
        super().__init__(e)

class NoPlayer(BotError):
    def __init__(self) -> None:
        super().__init__(f'There isn\'t an active player in your server.')

class FullVoiceChannel(BotError):
    def __init__(self, ctx : commands.Context) -> None:
        super().__init__(f'I can\'t join {ctx.author.voice.channel.mention}, because it\'s full.')

class NotAuthorized(BotError):
    def __init__(self) -> None:
        super().__init__("You cannot perform this action.")

class IncorrectChannelError(BotError):
    def __init__(self, ctx : commands.Context) -> None:
        player = ctx.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        channel = ctx.bot.get_channel(int(player.channel_id))
        super().__init__(f'{ctx.author.mention}, you must be in {channel.mention} for this session.')
class IncorrectTextChannelError(BotError):
    def __init__(self, ctx : commands.Context) -> None:
        player = ctx.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        channel = ctx.bot.get_channel(int(player.text_channel))
        super().__init__(f'{ctx.author.mention}, you can only use commands in {channel.mention} for this session.')

class AlreadyConnectedToChannel(BotError):
    def __init__(self) -> None:
        super().__init__("Already connected to a voice channel.")

class NoVoiceChannel(BotError):
    def __init__(self) -> None:
        super().__init__("I'm not connected to any voice channels.")

class QueueIsEmpty(BotError):
    def __init__(self) -> None:
        super().__init__("There are no tracks in the queue.")

class NoCurrentTrack(BotError):
    def __init__(self) -> None:
        super().__init__("There is no track currently playing.")

class PlayerIsAlreadyPaused(BotError):
    def __init__(self) -> None:
        super().__init__("The current track is already paused.")

class PlayerIsNotPaused(BotError):
    def __init__(self) -> None:
        super().__init__("The current track is not paused.")

class NoMoreTracks(BotError):
    def __init__(self) -> None:
        super().__init__("There are no more tracks in the queue.")

class InvalidTimeString(BotError):
    def __init__(self) -> None:
        super().__init__("The Time String Given is an Invalid one.")

class NoPerms(BotError):
    def __init__(self) -> None:
        super().__init__("I don't have permissions to `CONNECT` or `SPEAK`.")

class NoConnection(BotError):
    def __init__(self) -> None:
        super().__init__("You must be connected to a voice channel to use voice commands.")

class AfkChannel(BotError):
    def __init__(self) -> None:
        super().__init__("I can't play music in the afk channel.")

class NotAuthorized(BotError):

    def __init__(self) -> None:
        super().__init__("You cannot perform this action.")

# class SkipInLoopMode(BotError):
#     def __init__(self) -> None:
#         super().__init__(e)

class InvalidTrack(BotError):
    def __init__(self) -> None:
        super().__init__("Can't perform action on track that is out of the queue.")

class InvalidPosition(BotError):
    def __init__(self) -> None:
        super().__init__("Can't perform action with invalid position in the queue.")

class InvalidVolume(BotError):
    def __init__(self) -> None:
        super().__init__('Please enter a value between 1 and 100')

class OutOfTrack(BotError):
    def __init__(self) -> None:
        super().__init__('Can\'t seek out of the track')

class NegativeSeek(BotError):
    def __init__(self) -> None:
        super().__init__('Can\'t seek on negative timestamp')