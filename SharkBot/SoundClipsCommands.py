from discord.ext import commands
from SoundClips import SoundClips


class SoundClipsCommands(commands.Cog):
    """
    Plays a file from the local filesystem
    Commands (all take one argument, the search query): 
        yoda, ewok, chewbacca, jabba, leia, hansolo, roshi,
        oogway, sid, shifu, chunk, docholiday, kuzco, majorpayne,
        birthday
    """

    def __init__(self):
        self.sound_clips = SoundClips()

    @commands.command()
    async def yoda(self, ctx, *, query='Do or do not'):
        await self.sound_clips.play(ctx, query, 'Yoda')

    @commands.command()
    async def ewok(self, ctx, *, query='Shout'):
        await self.sound_clips.play(ctx, query, 'Ewok')

    @commands.command()
    async def chewbacca(self, ctx, *, query='Shout'):
        await self.sound_clips.play(ctx, query, 'Chewbacca')

    @commands.command()
    async def jabba(self, ctx, *, query='Laugh'):
        await self.sound_clips.play(ctx, query, 'Jabba')

    @commands.command()
    async def leia(self, ctx, *, query='Help me'):
        await self.sound_clips.play(ctx, query, 'Leia')

    @commands.command()
    async def hansolo(self, ctx, *, query='Never tell me the odds'):
        await self.sound_clips.play(ctx, query, 'Hansolo')

    @commands.command()
    async def roshi(self, ctx, *, query='Laugh'):
        await self.sound_clips.play(ctx, query, 'Roshi')

    @commands.command()
    async def oogway(self, ctx, *, query='Present'):
        await self.sound_clips.play(ctx, query, 'Oogway')

    @commands.command()
    async def sid(self, ctx, *, query='I choose life'):
        await self.sound_clips.play(ctx, query, 'Sid')

    @commands.command()
    async def shifu(self, ctx, *, query='Level zero'):
        await self.sound_clips.play(ctx, query, 'Shifu')

    @commands.command()
    async def chunk(self, ctx, *, query='Chocolate eruption'):
        await self.sound_clips.play(ctx, query, 'Chunk')

    @commands.command()
    async def docholiday(self, ctx, *, query='Huckleberry'):
        await self.sound_clips.play(ctx, query, 'Docholiday')

    @commands.command()
    async def kuzco(self, ctx, *, query='credit'):
        await self.sound_clips.play(ctx, query, 'Kuzco')

    @commands.command()
    async def majorpayne(self, ctx, *, query='Laugh'):
        await self.sound_clips.play(ctx, query, 'Majorpayne')

    @commands.command()
    async def birthday(self, ctx):
        await ctx.send('HAPPY BIRTHDAY LIL REY!!', tts=True)
