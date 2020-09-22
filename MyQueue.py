import asyncio
from async_timeout import timeout
import discord
import emoji
import random
import inspect
from YoutubeConvert import YTDLSource


class MusicPlayer:

    def __init__(self, ctx):
        self.ctx = ctx
        self.bot = ctx.bot
        self.cog = ctx.cog
        self.guild = ctx.guild
        self.volume = 25.0
        self.add_queue_counter = 0
        self.play_next_queue_counter = -1

        self.queue = asyncio.PriorityQueue(maxsize=100)
        self.play_next_song = asyncio.Event()

        self.bot.loop.create_task(self.player_loop())
        self.current_song = None


    async def player_loop(self):
        while True:
            self.play_next_song.clear()
            self.current_song = None
            try:
                async with timeout(600):
                    print('getting next song')
                    self.current_song = (await self.queue.get())[1]
                    print('got the song')
            except asyncio.TimeoutError:
                print('destroying queue')
                return await self.destroy()
            
            self.ctx.voice_client.play(self.current_song, after=lambda _: self.toggle_next())
            self.ctx.voice_client.source.volume = self.volume / 100
            await self.display_song_message(self.current_song, self.current_song.requester)
            await self.play_next_song.wait()


    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)


    async def display_song_message(self, song, username):
        notes = emoji.emojize(':notes:')
        song_status = ['Now playing: ', 'Requested by: ']
        if inspect.stack()[1][3] == 'skip':
            song_status = ['Skipped: ', 'Skipped by: ']
        elif inspect.stack()[1][3] == 'add':
            song_status = ['Queued: ', 'Queued by: ']
        elif inspect.stack()[1][3] == 'play':
            song_status = ['Queued in front: ', 'Queued by: ']
        elif inspect.stack()[1][3] == 'replay':
            song_status = ['Replay: ', 'Requested by: ']
        embed = discord.Embed(title=f'{notes}{song_status[0]}{song.title}{notes}', color=0x0000CD)
        embed.add_field(name=song_status[1], value=f'{username}', inline=False)
        await self.ctx.send(embed=embed)


    async def destroy(self):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self.cog.cleanup(self.guild))


    async def replay(self):
        """
        Does not work if the queue is at maxsize
        Need to make a copy of the current song since x is a reference to it
        """
        # Used to create a copy of the youtube object
        player = await YTDLSource.from_url(self.ctx, self.current_song.url, loop=self.bot.loop, stream=True)
        try:
            self.queue.put_nowait((self.play_next_queue_counter, player))
        except asyncio.QueueFull:
            return await self.ctx.send('Too many items queued!\nCannot replay this song')

        self.play_next_queue_counter -= 1
        await self.display_song_message(player, self.ctx.author.name)


    async def shuffle(self):
        """
        Obtain a list of players from the queue
        Create a list of randomly sampled priority values from the players
        Push players back into queue with new priority values
        """
        list_of_players = [(await self.queue.get()) for i in range(self.queue.qsize())]
        random_priorities = random.sample(range(0, len(list_of_players)), len(list_of_players))
        for priority,player in enumerate(list_of_players):
            track = (random_priorities[priority], player[1])
            self.queue.put_nowait(track)
        await self.ctx.send('Queue successfully shuffled!')


    async def currently_playing(self):
        await self.display_song_message(self.current_song, self.ctx.author.name)
