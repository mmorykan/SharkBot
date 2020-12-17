import asyncio
import emoji
import discord
from discord.ext import commands
from MyQueue import MusicPlayer
from YoutubeConvert import YTDLSource


class Music(commands.Cog):
    """
    Creates a music queue for each guild that SharkBot is a member of.
    Exposes all commands related to music available to users.
    Need to put ffmpeg in path environment variable in order to omit executable argument.
    Need a party time command for raves.
    Commands: play <url>, add <url>, replay, shuffle,
              now, show, pause, resume, skip,
              volume, connect, disconnect
    """

    def __init__(self, bot):
        """Initialize the players dict mapping guild ids to MusicPlayer objects"""

        self.bot = bot
        self.players = {}

    @commands.command()
    async def play(self, ctx, *, url='angel wings avianna acid'):
        """
        Streams from a url or search query. Does not download audio file. Adds song to front of queue.
        :param url: The search query to look up on Youtube
        :type url: str, variable length
        """

        if await self.ensure_voice(ctx):  # Make sure there is a voice client before modifying queue
            await self.add_to_queue(ctx, url, ['Queued in front: ', 'Queued by: '], True)

    @commands.command()
    async def add(self, ctx, *, url='angel wings avianna acid'):
        """
        Streams from a url or search query. Does not download audio file. Adds song to back of queue.
        :param url: The search query to look up on Youtube
        :type url: str, variable length
        """

        if await self.ensure_voice(ctx):  # Make sure there is a voice client before modifying queue
            await self.add_to_queue(ctx, url, ['Queued ', 'Queued by: '], False)

    @commands.command()
    async def replay(self, ctx):
        """Replay the currently playing song by pushing the same player back into the front of the queue"""

        correct_guild = self.get_correct_guild(ctx)  # Get the guild's queue
        async def add_song():  # Create function to interact with the queue
            await self.add_to_queue(ctx, correct_guild.current_song.data['webpage_url'], ['Replay: ', 'Requested by: '], True)

        voice_state = self.in_correct_voice_state(ctx)  # voice_client to play source
        has_song = correct_guild.get_current_song  # Is there a song currently playing
        error = 'No song to replay'  # If there is no song playing
        await self.interact_with_queue(ctx, voice_state, has_song, add_song, error)

    @commands.command()
    async def shuffle(self, ctx): 
        """Shuffle the queue"""

        correct_guild = self.get_correct_guild(ctx)
        voice_state = self.in_correct_voice_state(ctx)
        has_songs = correct_guild.get_queue_list  # Are there songs in the queue
        shuffle = correct_guild.shuffle  # Internal queue command
        error = 'Queue is empty'  # If the queue is empty
        await self.interact_with_queue(ctx, voice_state, has_songs, shuffle, error)
    
    @commands.command()
    async def now(self, ctx):
        """Get the currently playing song"""

        correct_guild = self.get_correct_guild(ctx)
        async def display_song():  # Set up display message function call
            await correct_guild.display_song_message(['Now playing: ', 'Requested by: '])

        voice_state = self.voice_is_connected(ctx)  # Is there a voice client
        has_song = correct_guild.get_current_song
        error = 'There is no song playing'
        
        await self.interact_with_queue(ctx, voice_state, has_song, display_song, error)

    @commands.command()
    async def show(self, ctx):
        """Show every song in the queue"""

        correct_guild = self.get_correct_guild(ctx)
        voice_state = self.voice_is_connected(ctx)
        has_songs = correct_guild.get_queue_list
        display_queue = correct_guild.show_queue  # Internal queue command to display whole queue
        error = 'The queue is empty'
        await self.interact_with_queue(ctx, voice_state, has_songs, display_queue, error)

    @commands.command(aliases=['stop'])
    async def pause(self, ctx):
        """Pause the audio source"""

        voice_state = self.in_correct_voice_state(ctx)
        is_playing = lambda: ctx.voice_client.is_playing()  # Is the source playing
        pause = lambda: ctx.voice_client.pause()  # pause the source
        error = 'I was not playing anything'
        await self.interact_with_queue(ctx, voice_state, is_playing, pause, error)

    @commands.command()
    async def resume(self, ctx):
        """Resume the paused audio source"""

        voice_state = self.in_correct_voice_state(ctx)
        is_paused = lambda: ctx.voice_client.is_paused()  # Is audio source paused
        resume = lambda: ctx.voice_client.resume()  # Resume audio source
        error = 'I was not paused'
        await self.interact_with_queue(ctx, voice_state, is_paused, resume, error)

    @commands.command()
    async def skip(self, ctx):
        """Skip the currently playing song"""

        correct_guild = self.get_correct_guild(ctx)
        async def stop_and_display_skip():  # Stop the audio source and display skip message
            ctx.voice_client.stop()
            await correct_guild.display_song_message(['Skipped: ', 'Skipped by: '], username=ctx.author.name)

        voice_state = self.in_correct_voice_state(ctx)
        can_stop_and_display_skip = lambda: ctx.voice_client.is_playing() or ctx.voice_client.is_paused()
        error = 'I was not playing anything'
        await self.interact_with_queue(ctx, voice_state, can_stop_and_display_skip, stop_and_display_skip, error)

    @commands.command()
    async def volume(self, ctx, volume: float=10.0):
        """
        Change the volume of the audio source because is inherits discord.PCMVolumeTransformer.
        :param volume: The volume to change audio source to
        :type volume: float
        """

        async def change_volume():  # Change volume with success message
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f'Changed volume to {volume}')

        voice_state = self.in_correct_voice_state(ctx)
        can_change_volume = lambda: 0 <= volume <= 100  
        error = 'My volume level must be between 0 and 100'
        await self.interact_with_queue(ctx, voice_state, can_change_volume, change_volume, error)

    @commands.command()
    async def connect(self, ctx):
        """Connecte the voice client to the voice channel"""

        if self.user_voice_is_connected(ctx):
            if self.voice_is_connected(ctx):
                if self.in_same_channel(ctx):
                    await ctx.send('Hey I\'m already connected')
                else:
                    await self.cleanup(ctx)  # Disconnect and delete previous existing queue
                    await ctx.author.voice.channel.connect()
                    self.create_queue(ctx)  # Create a new queue
            else:
                await ctx.author.voice.channel.connect()
                self.create_queue(ctx)
                on_join(ctx)
        else:
            await self.not_same_channel(ctx)

    @commands.command()
    async def disconnect(self, ctx):
        """Disconnect voice client from voice channel"""

        if self.in_correct_voice_state(ctx):
            await self.cleanup(ctx)
        else:
            await self.not_same_channel(ctx)
        

    async def ensure_voice(self, ctx):
        """Make sure there is a voice client connected. Connect if there isn't"""

        correct_voice_state = True
        if self.user_voice_is_connected(ctx):
            if self.voice_is_connected(ctx):
                if not self.in_same_channel(ctx):
                    await self.cleanup(ctx.guild)
                    await ctx.author.voice.channel.connect()
                    self.create_queue(ctx)
            else:
                await ctx.author.voice.channel.connect()
                self.create_queue(ctx)
        else:
            await self.not_same_channel(ctx)
            correct_voice_state = False

        return correct_voice_state

    async def interact_with_queue(self, ctx, voice_state, has_song, display_songs, error_message):
        """
        Generic method for interacting with the queue.
        :param voice_state: Is the voice client and user voice connected and in correct channel
        :type voice_state: bool
        :param has_song: Whether or not the queue is allowed to be modified
        :type has_song: function
        :param display_songs: Perform queue modification action. Await the function if coroutine
        :type display_songs: function, sometimes coroutine
        :param error_message: Message to send if unsuccessful queue modification
        :type error_message: str
        """

        if voice_state:
            if has_song():
                (await display_songs()) if asyncio.iscoroutinefunction(display_songs) else display_songs()
            else:
                sad = emoji.emojize(':disappointed:')  
                await ctx.send(f'{error_message}{sad}')
        else:
            await self.not_same_channel(ctx)

    async def add_to_queue(self, ctx, url, message, front):
        """
        Add a song to the guild's queue and display success message.
        :param url: the search query to type into Youtube
        :type url: str
        :param message: The message to include in the title of the success message
        :type message: str
        :param front: Whether or not the song goes in the front of the queue
        :type front: bool
        """

        correct_guild = self.get_correct_guild(ctx)
        async with ctx.typing():
            player = await YTDLSource.from_url(ctx, url, loop=self.bot.loop, stream=True)
        
        await correct_guild.update_queue(player, front)

        if correct_guild.current_song:
            await correct_guild.display_song_message(message, data=player.data)

    def get_correct_guild(self, ctx):
        """
        Obtain the correct queue
        :returns: The queue to modify
        :rtype: MusicPlayer
        """

        correct_guild = self.players.get(ctx.guild.id)
        if not correct_guild:
            self.create_queue(ctx)
        return self.players[ctx.guild.id]

    def create_queue(self, ctx):
        """Create a queue for the guild"""

        self.players[ctx.guild.id] = MusicPlayer(ctx)

    def in_correct_voice_state(self, ctx):
        """
        Make sure the voice client and the user's voice are connected to the same channel
        :returns: voice client connected and user's voice connected and both in same channel
        :rtype: bool
        """

        return self.voice_is_connected(ctx) and self.user_voice_is_connected(ctx) and self.in_same_channel(ctx)

    def voice_is_connected(self, ctx):
        return ctx.voice_client

    def user_voice_is_connected(self, ctx):
        return ctx.author.voice

    def in_same_channel(self, ctx):
        return ctx.voice_client.channel == ctx.author.voice.channel

    @staticmethod
    async def not_same_channel(ctx):
        await ctx.send('Oh no! I\'m not in this channel!')

    async def cleanup(self, ctx):
        """Disconnected the voice client and delete the guild's queue"""
        
        await ctx.voice_client.disconnect()
        del self.players[ctx.guild.id]

def on_join(ctx):
    """The sound clip to play as the voice client first connects"""

    source = '../SoundClips/GameboyStartup.m4a'
    player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source))
    ctx.voice_client.play(player)
