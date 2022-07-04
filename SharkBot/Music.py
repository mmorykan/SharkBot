import emoji
from MyQueue import MusicPlayer
from SoundClips import SoundClips


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

    def __init__(self):
        """Initialize the players dict mapping guild ids to MusicPlayer objects. Also load opus for AWS"""

        self.players = {}

    async def connect(self, ctx):
        """Connect the voice client to the voice channel"""
        
        if self.user_voice_is_connected(ctx):
            if self.voice_is_connected(ctx):
                if not self.in_same_channel(ctx):
                    await ctx.cog.cleanup(ctx)
                    await ctx.author.voice.channel.connect()
                    self.create_queue(ctx)
            else:
                await ctx.author.voice.channel.connect()
                self.create_queue(ctx)
        else:
            await self.not_same_channel(ctx)

    async def disconnect(self, ctx):
        """Disconnect voice client from voice channel"""

        await (ctx.cog.cleanup(ctx) if self.in_correct_voice_state(ctx) else self.not_same_channel(ctx))

    async def play(self, ctx, query, put_front=True, FromSource=SoundClips):
        """Connect voice client to channel, convert url to source, add source to queue"""

        await self.connect(ctx)
        await ctx.trigger_typing()
        source = await FromSource.get_source(ctx, query, self.get_correct_guild(ctx).volume)
        msg = ['Queued in front: ', 'Queued by: '] if put_front else ['Queued: ', 'Queued by: ']
        await self.add_to_queue(ctx, source, msg, put_front)

    def check_voice(error_msg):
        def check_voice_inner(queue_function):
            async def setup(self, ctx, volume=None):
                if self.in_correct_voice_state(ctx):
                    if not await queue_function(self, ctx=ctx, guild=self.get_correct_guild(ctx), volume=volume):
                        sad = emoji.emojize(':disappointed:')  
                        await ctx.send(f'{error_msg}{sad}')
                else:
                    await self.not_same_channel(ctx)

            return setup
        return check_voice_inner

    @check_voice('No song to replay')
    async def replay(self, **kwargs):
        """Replay the currently playing song by pushing the same player back into the front of the queue"""

        ctx, guild = kwargs['ctx'], kwargs['guild']
        current_song = guild.get_current_song()
        if current_song and current_song.data['webpage_url']:  # Cannot replay quotes
            await ctx.trigger_typing()
            source = await current_song.get_source(ctx, current_song.data['query'], guild.volume)
            await self.add_to_queue(ctx, source, ['Replay: ', 'Requested by: '], True)
            return True
        return False
 
    @check_voice('Queue is empty')
    async def shuffle(self, **kwargs): 
        """Shuffle the queue"""

        guild = kwargs['guild']
        if guild.get_song_list():
            await guild.shuffle()
            return True
        return False
    
    @check_voice('There is no song playing')
    async def now(self, **kwargs):
        """Get the currently playing song"""

        guild = kwargs['guild']
        if guild.get_current_song():
            await guild.display_song_message(['Now playing: ', 'Requested by: '])
            return True
        return False

    @check_voice('The queue is empty')
    async def show(self, **kwargs):
        """Show every song in the queue"""

        guild = kwargs['guild']
        if guild.get_song_list():
            await guild.show_queue()
            return True
        return False

    @check_voice('I was not playing anything')
    async def pause(self, **kwargs):
        """Pause the audio source"""

        ctx = kwargs['ctx']
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            return True
        return False

    @check_voice('I was not paused')
    async def resume(self, **kwargs):
        """Resume the paused audio source"""

        ctx = kwargs['ctx']
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            return True
        return False

    @check_voice('I was not playing anything')
    async def skip(self, **kwargs):
        """Skip the currently playing song"""

        ctx, guild = kwargs['ctx'], kwargs['guild']
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            ctx.voice_client.stop()
            await guild.display_song_message(['Skipped: ', 'Skipped by: '], username=ctx.author.name)
            return True
        return False

    @check_voice('I must be playing something and my volume level must be 0 - 100')
    async def volume(self, **kwargs):
        """
        Change the volume of the audio source because is inherits discord.PCMVolumeTransformer.
        :param volume: The volume*100 to change audio source to
        :type volume: float
        """

        ctx, guild, volume = kwargs['ctx'], kwargs['guild'], kwargs['volume']
        if 0 <= volume <= 100:
            guild.volume = volume / 100
            if ctx.voice_client.is_playing():
                ctx.voice_client.source.volume = volume / 100
            await ctx.send(f'Changed volume to {volume}')
            return True
        return False

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

        guild = self.get_correct_guild(ctx)

        await guild.update_queue(source, front)

        if guild.get_current_song():
            await guild.display_song_message(message, data=source.data)

    def get_correct_guild(self, ctx):
        """
        Obtain the correct queue
        :returns: The queue to modify
        :rtype: MusicPlayer
        """

        guild = self.players.get(ctx.guild.id)
        if not guild:
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

    async def not_same_channel(self, ctx):
        await ctx.send('Oh no! I\'m not in this channel!')
