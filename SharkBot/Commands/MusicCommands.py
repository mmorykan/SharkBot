from discord.ext import commands
from Commands.Audio import Audio


class MusicCommands(Audio):

    def __init__(self):
        super().__init__()

    @commands.command()
    async def play(self, ctx, *, url='cry by gryffin'):
        await self.music.play(ctx, url, ['Queued in front: ', 'Queued by: '], True)

    @commands.command()
    async def add(self, ctx, *, url='cry by gryffin'):
        await self.music.play(ctx, url, ['Queued: ', 'Queued by: '], False)

    @commands.command(aliases=['repeat'])
    async def replay(self, ctx):
        await self.music.replay(ctx)

    @commands.command()
    async def shuffle(self, ctx):
        await self.music.shuffle(ctx)

    @commands.command()
    async def now(self, ctx):
        await self.music.now(ctx)

    @commands.command()
    async def show(self, ctx):
        await self.music.show(ctx)

    @commands.command(aliases=['stop'])
    async def pause(self, ctx):
        await self.music.pause(ctx)

    @commands.command()
    async def resume(self, ctx):
        await self.music.resume(ctx)

    @commands.command()
    async def skip(self, ctx):
        await self.music.skip(ctx)

    @commands.command()
    async def volume(self, ctx, volume=10.0):
        await self.music.volume(ctx, volume)

    @commands.command()
    async def connect(self, ctx):
        await self.music.connect(ctx)

    @commands.command()
    async def disconnect(self, ctx):
        await self.music.disconnect(ctx)
