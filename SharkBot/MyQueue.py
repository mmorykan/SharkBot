import asyncio
from async_timeout import timeout
import discord
import emoji
import random


class MusicPlayer:
    """
    Represents an asyncio priority queue.
    Maintains a counter for priorities to discern whether songs should be in the front or in the back.
    Maintains a list as well as a priority queue in order to display the queue when asked.
    Creates a task to infinitely run the player_loop, looking for the next song.
    Ends task and deletes instance after being idle for 10 minutes.
    Uses asyncio Event to determine when to temporarily halt the loop and when to let it continue.
    Also displays messages and can shuffle the queue.
    """

    def __init__(self, ctx):
        """
        Initializes priority counters, queue list, priority queue, asyncio event, and the task
        """

        self.ctx = ctx
        self.bot = ctx.bot

        self.add_queue_counter = 0
        self.play_next_queue_counter = -1

        self.queue_list = []
        self.queue = asyncio.PriorityQueue(maxsize=100)
        self.play_next_song = asyncio.Event()

        self.task = self.bot.loop.create_task(self.player_loop())
        self.current_song = None

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
                    self.current_song = (await self.queue.get())[1]  # (priority, player)
                    self.queue_list.pop(0)  # Delete the song from the list
            except asyncio.TimeoutError:
                return await self.destroy()  # Deletes current instance

            self.ctx.voice_client.play(self.current_song, after=self.toggle_next)  # After is called after each song
            await self.display_song_message(['Now playing: ', 'Requested by: '])
            await self.play_next_song.wait()  # Make the loop wait until set is called in toggle_next, after the song has finished

    def toggle_next(self, error):
        """
        Sets the asyncio event so that the loop is no longer waiting for the song to finish
        :param error: Paramater to be raised if an exception occurs within the play function
        :type error: Exception
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

        random_priorities = random.sample(range(len(self.queue_list)), len(self.queue_list))
        queue = asyncio.PriorityQueue(maxsize=100)
        random_queue_list = []

        for i, (priority, player) in enumerate(self.queue_list):
            track = random_priorities[i], player
            queue.put_nowait(track)
            random_queue_list.append(track)  # Append to new list because tuples are immutable

        random_queue_list.sort(key=lambda player: player[0])  # Put songs in correct order by priority values

        self.queue_list = random_queue_list
        self.queue = queue
        await self.ctx.send('Queue successfully shuffled!')

    async def show_queue(self):
        """Display a message for every song in the queue"""

        for priority, player in self.queue_list:
            await self.display_song_message(['Queued: ', 'Queued by: '], player.data)

    async def update_queue(self, player, front):
        """
        Push the new player into the queue and update priority counters
        :param player: The audio track to be played
        :type player: YTDLSource
        :param front: Whether or not this song should be played next
        :type front: bool
        """
        
        counter = self.play_next_queue_counter if front else self.add_queue_counter
        item = counter, player  # player tuple

        try:
            self.queue.put_nowait(item)
        except asyncio.QueueFull:
            return await self.ctx.send(f'I cannot queue more than {correct_guild.queue.maxsize} songs')

        # Update list and counters
        if front:
            self.queue_list.insert(0, item)
            self.play_next_queue_counter -= 1
        else:
            self.queue_list.append(item)
            self.add_queue_counter += 1

    def get_queue_list(self):
        return self.queue_list

    def get_current_song(self):
        return self.current_song
