from discord.ext import commands
from Commands.Audio import Audio
from YoutubeConvert import YTDLSource


class MusicCommands(Audio):

    @commands.command()
    async def play(self, ctx, *, url='cry by gryffin'):
        await self.music.play(ctx, url, FromSource=YTDLSource)

    @commands.command()
    async def add(self, ctx, *, url='cry by gryffin'):
        await self.music.play(ctx, url, put_front=False, FromSource=YTDLSource)

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
