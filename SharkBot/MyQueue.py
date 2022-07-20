import discord
import emoji
import random
from asyncio import Event, TimeoutError, QueueFull, Queue
from async_timeout import timeout


class MusicPlayer:
    """
    Represents an asyncio queue.
    Creates a task to infinitely run the player_loop, looking for the next song.
    Ends task and deletes instance after being idle for 10 minutes.
    Uses asyncio Event to determine when to temporarily halt the loop and when to let it continue.
    Also displays messages and can shuffle the queue.
    """

    def __init__(self, ctx):
        """
        Initializes queue, asyncio event, and the task
        """

        self.ctx = ctx
        self.bot = ctx.bot

        self.queue = Queue(maxsize=100)
        self.play_next_song = Event()

        self.task = self.bot.loop.create_task(self.player_loop())
        self.current_song = None

        self.volume = 0.05

    async def player_loop(self):
        """
        This is the infinitely looping task looking for songs to play from the priotiry queue.
        Times out and deletes instance after 10 minutes of being idle.
        """

        while True:
            self.play_next_song.clear()  # Make the wait function block the loop
            self.current_song = None

            try:
                async with timeout(600):  # 10 minute timeout
                    self.current_song = await self.queue.get()
            except TimeoutError:
                return await self.destroy()  # Deletes current instance

            self.ctx.voice_client.play(self.current_song, after=self.toggle_next)  # After is called after each song
            await self.display_song_message(['Now playing: ', 'Requested by: '])
            await self.play_next_song.wait()  # Make the loop wait until set is called in toggle_next, after the song has finished

    def toggle_next(self, _):
        """
        Sets the asyncio event so that the loop is no longer waiting for the song to finish
        """

        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def display_song_message(self, descriptors, data=None, username=None):
        """
        Displays song title, song duration, song url, and requester using a discord Embed.
        :param descriptors: The text for the title of the Embed
        :type descriptors: list
        :param data: Provides all player information such as requester, duration, and url
        :type data: dict, optional
        :param username: The user who issued the command to display this message
        :type username: str, optional
        """

        if not data:
            data = self.current_song.data
        if not username:
            username = data['requester']

        notes = emoji.emojize(':notes:')
        title = data['title']
        embed = discord.Embed(title=f'{notes}{descriptors[0]}{title}{notes}', color=0x0000CD)
        embed.add_field(name=descriptors[1], value=username, inline=True)
        embed.add_field(name='Duration:', value=data['duration'], inline=True)
        embed.add_field(name='YouTube URL:', value=data['webpage_url'], inline=False)

        await self.ctx.send(embed=embed)

    async def destroy(self):
        """Disconnect voice client and delete this current instance."""

        await self.ctx.cog.cleanup(self.ctx)

    async def shuffle(self):
        """
        Create a list of randomly sampled priority values from the players
        Push players back into queue with new priority values
        """

        random.shuffle(self.queue._queue)
        await self.ctx.send('Queue successfully shuffled!')

    async def show_queue(self):
        """Display a message for every song in the queue"""

        for player in self.queue._queue:
            await self.display_song_message(['Queued: ', 'Queued by: '], player.data)

    async def update_queue(self, player, front):
        """
        Push the new player into the queue and update priority counters
        :param player: The audio track to be played
        :type player: YTDLSource
        :param front: Whether or not this song should be played next
        :type front: bool
        """

        try:
            self.queue.put_nowait(player)
        except QueueFull:
            await self.ctx.send(f'I cannot queue more than {self.queue.maxsize} songs')

    def get_song_list(self):
        return self.queue._queue

    def get_current_song(self):
        return self.current_song

    def __del__(self):
        self.task.cancel()
