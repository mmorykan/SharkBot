from discord.ext import commands
from Commands.Audio import Audio


class SoundClipsCommands(Audio):
    """
    Plays a file from the local filesystem
    Commands (all quotes take one argument, the search query): 
        yoda, ewok, chewbacca, jabba, leia, hansolo, roshi,
        oogway, sid, shifu, chunk, docholiday, kuzco, majorpayne,
        birthday
    """

    @commands.command()
    async def yoda(self, ctx, *, query='Do or do not'):
        await self.music.play_quote(ctx, query, 'Yoda')

    @commands.command()
    async def ewok(self, ctx, *, query='Shout'):
        await self.music.play_quote(ctx, query, 'Ewok')

    @commands.command()
    async def chewbacca(self, ctx, *, query='Shout'):
        await self.music.play_quote(ctx, query, 'Chewbacca')

    @commands.command()
    async def jabba(self, ctx, *, query='Laugh'):
        await self.music.play_quote(ctx, query, 'Jabba')

    @commands.command()
    async def leia(self, ctx, *, query='Help me'):
        await self.music.play_quote(ctx, query, 'Leia')

    @commands.command()
    async def hansolo(self, ctx, *, query='Never tell me the odds'):
        await self.music.play_quote(ctx, query, 'Hansolo')

    @commands.command()
    async def roshi(self, ctx, *, query='Laugh'):
        await self.music.play_quote(ctx, query, 'Roshi')

    @commands.command()
    async def oogway(self, ctx, *, query='Present'):
        await self.music.play_quote(ctx, query, 'Oogway')

    @commands.command()
    async def sid(self, ctx, *, query='I choose life'):
        await self.music.play_quote(ctx, query, 'Sid')

    @commands.command()
    async def shifu(self, ctx, *, query='Level zero'):
        await self.music.play_quote(ctx, query, 'Shifu')

    @commands.command()
    async def chunk(self, ctx, *, query='Chocolate eruption'):
        await self.music.play_quote(ctx, query, 'Chunk')

    @commands.command()
    async def docholiday(self, ctx, *, query='Huckleberry'):
        await self.music.play_quote(ctx, query, 'Docholiday')

    @commands.command()
    async def kuzco(self, ctx, *, query='credit'):
        await self.music.play_quote(ctx, query, 'Kuzco')

    @commands.command()
    async def majorpayne(self, ctx, *, query='Laugh'):
        await self.music.play_quote(ctx, query, 'Majorpayne')

    @commands.command()
    async def birthday(self, ctx):
        await ctx.send('HAPPY BIRTHDAY LIL REY!!', tts=True)
