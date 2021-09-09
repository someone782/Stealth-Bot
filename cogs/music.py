### THANKS TO DaPandaOfficial🐼#5684 FOR MAKING THIS AMAZING MUSIC COG ###

import re
import zlib
import json
import random
import discord
import lavalink
import datetime as dt
from discord.ext import commands, menus

lavalink_node_settings = ['lava.link', 80, 'anything as a password', 'eu', 'default-node']
bot_user_id = 788278464474120202
url_rx = re.compile(r'https?://(?:www\.)?.+')
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"


def setup(bot):
    bot.add_cog(SocketFix(bot))
    bot.add_cog(music(bot))


class FullVoiceChannel(commands.CommandError):
    pass


class IncorrectChannelError(commands.CommandError):
    pass


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoCurrentTrack(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class PlayerIsNotPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class InvalidTimeString(commands.CommandError):
    pass


class NoPerms(commands.CommandError):
    pass


class NoConnection(commands.CommandError):
    pass


class QueueMenu(menus.ListPageSource):
    """Player queue paginator class."""

    def __init__(self, entries, *, per_page=10):
        super().__init__(entries, per_page=per_page)

    async def format_page(self, menu: menus.Menu, info):
        embed = discord.Embed(title=f'Current queue:', color=0x2F3136)
        embed.description = '\n'.join(f'{info} \n' for index, info, in list(enumerate(info, 0)))
        return embed

    def is_paginating(self):
        # We always want to embed even on 1 page of results...
        return True


class music(commands.Cog):
    """
    🎵 Commands used to play music
    """

    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(760179628122964008)
            bot.lavalink.add_node(*lavalink_node_settings)  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_custom_receive')

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            await self.ensure_voice(ctx)
            #  Ensure that the bot and command author share a mutual voicechannel.

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.reply(error.original)

        if isinstance(error, IncorrectChannelError):
            return

        if isinstance(error, NoVoiceChannel):
            message = "I'm not connected to a voice channel."
            return await ctx.reply(message)

        if isinstance(error, AlreadyConnectedToChannel):
            message = "I'm already connected to a voice channel."
            return await ctx.reply(message)

        if isinstance(error, QueueIsEmpty):
            message = "There are no tracks in the queue."
            return await ctx.reply(message)

        if isinstance(error, PlayerIsAlreadyPaused):
            message = "The current track is already paused."
            return await ctx.reply(message)

        if isinstance(error, NoMoreTracks):
            message = "There are no more tracks in the queue."
            await ctx.reply(message)

        if isinstance(error, InvalidRepeatMode):
            message = "Available loop modes: `true` and `false`."
            await ctx.reply(message)

        if isinstance(error, NoCurrentTrack):
            message = "There is no track currently playing."
            await ctx.reply(message)

        if isinstance(error, FullVoiceChannel):
            message = f'I can\'t join {ctx.author.voice.channel.mention}, because it\'s full.'
            await ctx.reply(message)

        if isinstance(error, NoPerms):
            message = "I don't have permissions to `CONNECT` or `SPEAK`."
            await ctx.reply(message)

        if isinstance(error, NoConnection):
            message = "You must be connected to a voice channel to use voice commands."
            await ctx.reply(message)

        if isinstance(error, PlayerIsNotPaused):
            message = "The current track is not paused."
            return await ctx.reply(message)

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise NoConnection()

        if not player.is_connected:
            if not should_connect:
                raise NoVoiceChannel()

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)
            if ctx.author.voice.channel.user_limit != 0:
                limit = ctx.author.voice.channel.user_limit
                if len(ctx.author.voice.channel.members) == limit:
                    raise FullVoiceChannel()
            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise NoPerms()

            player.store('channel', ctx.channel)
            player.store('dj', ctx.author)
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                message = f'{ctx.author.mention}, you must be in {player.channel.mention} for this session.'
                await ctx.reply(message)
                raise IncorrectChannelError()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        if member.bot:
            return

        player = self.bot.lavalink.player_manager.get(member.guild.id)
        if player is None:
            return
        if not player.channel_id or not player:
            self.bot.lavalink.player_manager.remove(member.guild.id)
            return
        channel = self.bot.get_channel(int(player.channel_id))
        if member == player._user_data['dj'] and after.channel is None:
            for m in channel.members:
                if m.bot:
                    continue
                else:
                    player._user_data['dj'] = m
                    return

        elif after.channel == channel and player._user_data['dj'] not in channel.members:
            player._user_data['dj'] = member

        if player.is_connected:
            if len(channel.members) == 1:
                player.queue.clear()
                await player.stop()
                await member.guild.change_voice_state(channel=None)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)
            await guild.change_voice_state(channel=None)

    def is_privileged(self, ctx: commands.Context):
        """Check whether the user is an Admin or DJ."""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if player._user_data['dj'] == ctx.author:
            return 'DJ'
        if ctx.author.guild_permissions.administrator:
            return 'ADMIN'
        else:
            return False

    @commands.command(help="Adds a song to queue", aliases=['p', 'sing'])
    async def play(self, ctx, *, query: str):
        """Loads your input and adds it to the queue; If there is no playing track, then it will start playing"""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)

        # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
        # Alternatively, results['tracks'] could be an empty array if the query yielded no tracks.
        if not results or not results['tracks']:
            embed_var = discord.Embed(color=0x2F3136)
            embed_var.description = 'No songs were found with that query. Please try again.'
            return await ctx.reply(embed=embed_var)

        embed = discord.Embed(color=0x2F3136)

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if results['loadType'] == 'NO_MATCHES':
            embed_var = discord.Embed(color=0x2F3136)
            embed_var.description = 'No songs were found with that query. Please try again.'
            return await ctx.reply(embed=embed_var)
        if results['loadType'] == 'LOAD_FAILED':
            embed_var = discord.Embed(color=0x2F3136)
            embed_var.description = 'Failed loading your song.'
            return await ctx.reply(embed=embed_var)
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author, track=track)

            embed.description = f'Queued [{results["tracks"][0]["info"]["title"]}]' \
                                f'({results["tracks"][0]["info"]["uri"]}) with {len(tracks)} songs.'
        else:
            track = results['tracks'][0]
            embed.description = f'Queued [{track["info"]["title"]}]({track["info"]["uri"]}) - [{ctx.author.mention}]'
            track = lavalink.models.AudioTrack(track, ctx.author, recommended=True)
            player.add(requester=ctx.author, track=track)

        await ctx.reply(embed=embed)

        if not player.is_playing:
            await player.play()

    @commands.command(help="Leaves the current voice channel", aliases=['dc', 'leave', 'fuckoff', 'dis'])
    async def disconnect(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "I'm not connected to any voice channels."
            return await ctx.reply(embed=embed)

        if self.is_privileged(ctx) == 'DJ':
            embed = discord.Embed(color=0x2F3136)
            embed.description = 'The DJ has disconnected the player.'
            player.queue.clear()
            await player.stop()
            await ctx.guild.change_voice_state(channel=None)
            return await ctx.reply(embed=embed)

        if self.is_privileged(ctx) == 'ADMIN':
            embed = discord.Embed(color=0x2F3136)
            embed.description = 'An Admin has disconnected the player.'
            player.queue.clear()
            await player.stop()
            await ctx.guild.change_voice_state(channel=None)
            return await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "Only the DJ or an Admin can perform this action."
            return await ctx.reply(embed=embed)

    @commands.command(help="Pauses the current song", aliases=['pa'])
    async def pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if self.is_privileged(ctx) == 'DJ':
            if player.paused:
                raise PlayerIsAlreadyPaused
            await player.set_pause(True)
            embed = discord.Embed(color=0x2F3136)
            embed.description = "The playback was paused by the DJ"
            return await ctx.reply(embed=embed)

        if self.is_privileged(ctx) == 'ADMIN':
            if player.paused:
                raise PlayerIsAlreadyPaused
            await player.set_pause(True)
            embed = discord.Embed(color=0x2F3136)
            embed.description = "The playback was paused by an Admin."
            return await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "Only the DJ or an Admin can perform this action."
            return await ctx.reply(embed=embed)

    @commands.command(help="Resumes the current song", aliases=['re', 'continue', 'unpause'])
    async def resume(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if self.is_privileged(ctx) == 'DJ':
            if not player.paused:
                raise PlayerIsNotPaused()
            await player.set_pause(False)
            embed = discord.Embed(color=0x2F3136)
            embed.description = "The playback was resumed by the DJ"
            return await ctx.reply(embed=embed)

        if self.is_privileged(ctx) == 'ADMIN':
            if not player.paused:
                raise PlayerIsNotPaused()
            await player.set_pause(False)
            embed = discord.Embed(color=0x2F3136)
            embed.description = "The playback was resumed by an Admin."
            return await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "Only the DJ or an Admin can perform this action."
            return await ctx.reply(embed=embed)

    @commands.command(help="Stops the current song and removes all songs in queue", aliases=['st'])
    async def stop(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if self.is_privileged(ctx) == 'DJ':
            player.queue.clear()
            await player.stop()
            embed = discord.Embed(color=0x2F3136)
            embed.description = "The playback was stopped by the DJ."
            return await ctx.reply(embed=embed)

        if self.is_privileged(ctx) == 'ADMIN':
            player.queue.clear()
            await player.stop()
            embed = discord.Embed(color=0x2F3136)
            embed.description = "The playback was stopped by an Admin."
            return await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "Only the DJ or an Admin can perform this action."
            return await ctx.reply(embed=embed)

    @commands.command(help="Removes all songs from the queue", aliases=['rem'])
    async def remove(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if self.is_privileged(ctx) == 'DJ':
            if not len(player.queue) > 0:
                raise QueueIsEmpty()
            player.queue.clear()
            embed = discord.Embed(color=0x2F3136)
            embed.description = "The playback was stopped by the DJ."
            return await ctx.reply(embed=embed)

        if self.is_privileged(ctx) == 'ADMIN':
            player.queue.clear()
            embed = discord.Embed(color=0x2F3136)
            embed.description = "The playback was stopped by an Admin."
            return await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "Only the DJ or an Admin can perform this action."
            return await ctx.reply(embed=embed)

    @commands.command(help="Skips the current song to the next one in queue", aliases=['next', 'sk'])
    async def skip(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if self.is_privileged(ctx) == 'DJ':
            if len(player.queue) == 0:
                raise NoMoreTracks
            await player.skip()
            embed = discord.Embed(color=0x2F3136)
            embed.description = "The current track was skipped by the DJ."
            return await ctx.reply(embed=embed)

        if self.is_privileged(ctx) == 'ADMIN':
            if not len(player.queue) == 0:
                raise NoMoreTracks
            await player.skip()
            embed = discord.Embed(color=0x2F3136)
            embed.description = "The current track was skipped by an Admin."
            return await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "Only the DJ or an Admin can perform this action."
            return await ctx.reply(embed=embed)

    @commands.command(help="Shuffles the entire queue", aliases=['random'])
    async def shuffle(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if self.is_privileged(ctx) == 'DJ':
            random.shuffle(player.queue)
            embed = discord.Embed(color=0x2F3136)
            embed.description = "The current queue was shuffled by the DJ."
            return await ctx.reply(embed=embed)

        if self.is_privileged(ctx) == 'ADMIN':
            random.shuffle(player.queue)
            embed = discord.Embed(color=0x2F3136)
            embed.description = "The current queue was shuffled by an Admin."
            return await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "Only the DJ or an Admin can perform this action."
            return await ctx.reply(embed=embed)

    @commands.command(help="Loops the queue", aliases=['repeat'])
    async def loop(self, ctx, mode: bool = None):
        prefix = await self.bot.db.fetchval('SELECT prefix FROM guilds WHERE guild_id = $1', ctx.guild.id)
        prefix = prefix or 'sb!'
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "I'm not connected to any voice channels."
            return await ctx.reply(embed=embed)

        if not mode:
            embed = discord.Embed(color=0x2F3136)
            embed.description = f"Current loop mode: `{player.repeat}`. To change this do `{prefix}loop on/off`"
            return await ctx.reply(embed=embed)

        if self.is_privileged(ctx) in ('DJ', 'ADMIM'):
            player.set_repeat(mode)

            embed = discord.Embed(color=0x2F3136)
            embed.description = f"The {self.is_privileged(ctx)} has set loop mode to `{mode}`."
            return await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "Only the DJ or an Admin can perform this action."
            return await ctx.reply(embed=embed)

    @commands.command(help="Shows you the queue", aliases=['q', 'que', 'list', 'upcoming'])
    async def queue(self, ctx: commands.Context):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            raise NoVoiceChannel()

        if len(player.queue) == 0:
            raise QueueIsEmpty()

        info = [
            f'**Now Playing:** \n[{player.current.title}]({player.current.uri}) | '
            f'Requested by: {player.current.requester.mention} \n**Upcoming:**']
        index = 0
        for x in player.queue:
            index += 1
            info.append(
                f'`{index}.` [{x.title.upper()}]({x.uri}) - {str(dt.timedelta(milliseconds=int(x.duration)))} '
                f'| Requested by: {x.requester.mention}')
        pages = QueueMenu(entries=info)
        paginator = menus.MenuPages(source=pages, timeout=None, delete_message_after=True)

        await paginator.start(ctx)

    @commands.command(help="Shows information about the current song", aliases=['np', 'playing', 'now_playing', 'track', 'current'])
    async def nowplaying(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            raise NoCurrentTrack
        thumnail = f"https://img.youtube.com/vi/{player.current.identifier}/maxresdefault.jpg"
        embed = discord.Embed(title='Now playing', timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_image(url=thumnail)
        # embed.add_field(name="Current Track:", value=f'**[{player.current.title.upper()}]({player.current.uri})**',
        #                 inline=False)
        # embed.add_field(name="Artist:", value=f'{player.current.author}\n_ \u200b _', inline=True)
        # embed.add_field(name='Duration:',
        #                 value=f'{str(dt.timedelta(milliseconds=int(player.current.duration)))}\n_ \u200b _',
        #                 inline=True)

        embed.description = f"""
Song name: [{player.current.title.upper()}]({player.current.uri})
Artist: {player.current.author}
Duration: {str(dt.timedelta(milliseconds=int(player.current.duration)))}
Requested by: {player.current.requester.mention}
        """

        #embed.add_field(name='Requested By:', value=f'{player.current.requester.mention}\n_ \u200b _', inline=True)
        if len(player.queue) > 0:
            # embed.add_field(name='Next Track:', value=f'**[{player.queue[0].title.upper()}]({player.queue[0].uri})**',
            #                 inline=False)
            # embed.add_field(name="Artist:", value=f'{player.queue[0].author}\n_ \u200b _', inline=True)
            # embed.add_field(name='Duration:',
            #                 value=f'{str(dt.timedelta(milliseconds=int(player.queue[0].duration)))}\n_ \u200b _',
            #                 inline=True)
            # embed.add_field(name='Requested By:', value=f'{player.queue[0].requester.mention}\n_ \u200b _', inline=True)

            embed.description = f"""
Next song name: [{player.queue[0].title.upper()}]({player.queue[0].uri})
Artist: {player.queue[0].author}
Duration: {str(dt.timedelta(milliseconds=int(player.queue[0].duration)))}
Requested by: {player.queue[0].requester.mention}
            """

        embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    @commands.command(help="Restarts the songs in the queue", aliases=['res'])
    async def restart(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if self.is_privileged(ctx) in ('DJ', 'ADMIN'):
            if not player.current:
                raise NoCurrentTrack()
            await player.seek(0)
            embed = discord.Embed(color=0x2F3136)
            embed.description = f"The {self.is_privileged(ctx)} has restarted the current track."
            return await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "Only the DJ or an Admin can perform this action."
            return await ctx.reply(embed=embed)

    @commands.command(help="Seeks to a certain point in the current song")
    async def seek(self, ctx, position : str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if self.is_privileged(ctx) in ('DJ', 'ADMIN'):
            if not player.current:
                raise NoCurrentTrack()
            if not (match := re.match(TIME_REGEX, position)):
                raise InvalidTimeString
            if match.group(3):
                secs = (int(match.group(1)) * 60) + (int(match.group(3)))
            else:
                secs = int(match.group(1))
            await player.seek(secs * 1000)
            embed = discord.Embed(color=0x2F3136)
            embed.description = f"The {self.is_privileged(ctx)} has seeked the current track to {position}."

            return await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "Only the DJ or an Admin can perform this action."
            return await ctx.reply(embed=embed)

    @commands.command(help="Changes the current volume", aliases=['vol'])
    async def volume(self, ctx, volume : int = None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "I'm not connected to any voice channels "
            return await ctx.reply(embed=embed)

        if volume is None:
            embed = discord.Embed(color=0x2F3136)
            embed.description = f'Current volume: `{player.volume}`.'
            return await ctx.reply(embed=embed)

        if self.is_privileged(ctx) == 'DJ':
            if not 0 < volume < 101:
                embed = discord.Embed(color=0x2F3136)
                embed.description = 'Please enter a value between `1` and `100`.'
                return await ctx.reply(embed=embed)

            await player.set_volume(volume)
            embed = discord.Embed(color=0x2F3136)
            embed.description = f'The volume was set to `{volume}` by the DJ.'
            return await ctx.reply(embed=embed)

        if self.is_privileged(ctx) == 'ADMIN':
            if not 0 < volume < 101:
                embed = discord.Embed(color=0x2F3136)
                embed.description = 'Please enter a value between `1` and `100`.'
                return await ctx.reply(embed=embed)

            await player.set_volume(volume)
            embed = discord.Embed(color=0x2F3136)
            embed.description = f'The volume was set to `{volume}` by an Admin.'
            return await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(color=0x2F3136)
            embed.description = "Only the DJ or an Admin can perform this action."
            return await ctx.reply(embed=embed)


class SocketFix(commands.Cog):
    """
    Class to dispatch socket events
    """
    def __init__(self, bot):
        self.bot = bot

        self._zlib = zlib.decompressobj()
        self._buffer = bytearray()

    @commands.Cog.listener()
    async def on_socket_raw_receive(self, msg):
        """ This is to replicate discord.py's 'on_socket_response' that was removed from discord.py v2 """
        if type(msg) is bytes:
            self._buffer.extend(msg)

            if len(msg) < 4 or msg[-4:] != b'\x00\x00\xff\xff':
                return

            try:
                msg = self._zlib.decompress(self._buffer)
            except Exception:
                self._buffer = bytearray()  # Reset buffer on fail just in case...
                return

            msg = msg.decode('utf-8')
            self._buffer = bytearray()

        msg = json.loads(msg)
        self.bot.dispatch('socket_custom_receive', msg)
