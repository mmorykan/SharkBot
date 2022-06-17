import asyncio
import emoji
from MyQueue import MusicPlayer
from YoutubeConvert import YTDLSource


class Music:
    """
    Creates a music queue for each guild that SharkBot is a member of.
    Exposes all commands related to music available to users.
    Need to put ffmpeg in path environment variable in order to omit executable argument.
    Need a party time command for raves.
    Commands: replay, shuffle,
              now, show, pause, resume, skip,
              volume, connect, disconnect
    """

    players = {}

    def __init__(self):
        """Initialize the players dict mapping guild ids to MusicPlayer objects. Also load opus for AWS"""

        pass        
        # discord.opus.load_opus('/home/linuxbrew/.linuxbrew/Cellar/opus/1.3.1/lib/libopus.so')  # Needed on AWS because ctypes.util.find_library('opus') only returns filename, not the path

    async def connect(self, ctx):
        """Connect the voice client to the voice channel"""
        
        if self.user_voice_is_connected(ctx):
            if self.voice_is_connected(ctx):
                if not self.in_same_channel(ctx):
                    # await ctx.send('Hey I\'m already connected')
                # else:
                    await self.cleanup(ctx)  # Disconnect and delete previous existing queue
                    await ctx.author.voice.channel.connect()
                    self.create_queue(ctx)  # Create a new queue
            else:
                await ctx.author.voice.channel.connect()
                self.create_queue(ctx)
        else:
            await self.not_same_channel(ctx)

    async def disconnect(self, ctx):
        """Disconnect voice client from voice channel"""

        await (self.cleanup(ctx) if self.in_correct_voice_state(ctx) else self.not_same_channel(ctx))

    async def play(self, ctx, url, msg, put_front):
        """Connect voice client to channel, convert url to source, add source to queue"""

        await self.connect(ctx)
        async with ctx.typing():
            source = await YTDLSource.from_url(ctx, url, loop=ctx.bot.loop)
            await self.add_to_queue(ctx, source, msg, put_front)
        
    async def replay(self, ctx):
        """Replay the currently playing song by pushing the same player back into the front of the queue"""

        correct_guild = self.get_correct_guild(ctx)  # Get the guild's queue
        async def add_song():  # Create function to interact with the queue
            await self.add_to_queue(ctx, 
            await YTDLSource.from_url(ctx, correct_guild.current_song.data['webpage_url'], loop=ctx.bot.loop),
            ['Replay: ', 'Requested by: '], True)

        voice_state = self.in_correct_voice_state(ctx)  # voice_client to play source
        has_song = correct_guild.get_current_song  # Is there a song currently playing
        error = 'No song to replay'  # If there is no song playing
        await self.interact_with_queue(ctx, voice_state, has_song, add_song, error)

    async def shuffle(self, ctx): 
        """Shuffle the queue"""

        correct_guild = self.get_correct_guild(ctx)
        voice_state = self.in_correct_voice_state(ctx)
        has_songs = correct_guild.get_queue_list  # Are there songs in the queue
        shuffle = correct_guild.shuffle  # Internal queue command
        error = 'Queue is empty'  # If the queue is empty
        await self.interact_with_queue(ctx, voice_state, has_songs, shuffle, error)
    
    async def now(self, ctx):
        """Get the currently playing song"""

        correct_guild = self.get_correct_guild(ctx)
        async def display_song():  # Set up display message function call
            await correct_guild.display_song_message(['Now playing: ', 'Requested by: '])

        voice_state = self.voice_is_connected(ctx)  # Is there a voice client
        has_song = correct_guild.get_current_song
        error = 'There is no song playing'
        
        await self.interact_with_queue(ctx, voice_state, has_song, display_song, error)

    async def show(self, ctx):
        """Show every song in the queue"""

        correct_guild = self.get_correct_guild(ctx)
        voice_state = self.voice_is_connected(ctx)
        has_songs = correct_guild.get_queue_list
        display_queue = correct_guild.show_queue  # Internal queue command to display whole queue
        error = 'The queue is empty'
        await self.interact_with_queue(ctx, voice_state, has_songs, display_queue, error)

    async def pause(self, ctx):
        """Pause the audio source"""

        voice_state = self.in_correct_voice_state(ctx)
        is_playing = lambda: ctx.voice_client.is_playing()  # Is the source playing
        pause = lambda: ctx.voice_client.pause()  # pause the source
        error = 'I was not playing anything'
        await self.interact_with_queue(ctx, voice_state, is_playing, pause, error)

    async def resume(self, ctx):
        """Resume the paused audio source"""

        voice_state = self.in_correct_voice_state(ctx)
        is_paused = lambda: ctx.voice_client.is_paused()  # Is audio source paused
        resume = lambda: ctx.voice_client.resume()  # Resume audio source
        error = 'I was not paused'
        await self.interact_with_queue(ctx, voice_state, is_paused, resume, error)

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

    async def volume(self, ctx, volume):
        """
        Change the volume of the audio source because is inherits discord.PCMVolumeTransformer.
        :param volume: The volume to change audio source to
        :type volume: float
        """

        async def change_volume():
            ctx.voice_client.source.volume = YTDLSource._volume = volume / 100
            await ctx.send(f'Changed volume to {volume}')

        voice_state = self.in_correct_voice_state(ctx)
        can_change_volume = lambda: 0 <= volume <= 100  
        error = 'My volume level must be between 0 and 100'
        await self.interact_with_queue(ctx, voice_state, can_change_volume, change_volume, error)

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

    async def add_to_queue(self, ctx, source, message, front):
        """
        Adds source to queue with info message. Adds song to front or back of queue.
        :param source: The audio source to add to queue
        :type url: YTDLSource
        :param message: The message to include in the title of the success message
        :type message: str
        :param front: Whether or not the song goes in the front of the queue
        :type front: bool
        """

        correct_guild = self.get_correct_guild(ctx)

        await correct_guild.update_queue(source, front)

        if correct_guild.get_current_song():
            await correct_guild.display_song_message(message, data=source.data)

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

    async def not_same_channel(ctx):
        await ctx.send('Oh no! I\'m not in this channel!')

    async def cleanup(self, ctx):
        """Disconnected the voice client and delete the guild's queue"""
        
        await ctx.voice_client.disconnect()
        del self.players[ctx.guild.id]
