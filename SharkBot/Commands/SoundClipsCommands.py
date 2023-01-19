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

    defaults = {
        'yoda': 'Do or do not',
        'ewok': 'Shout',
        'chewbacca': 'Shout',
        'jabba': 'Laugh',
        'leia': 'Help me',
        'hansolo': 'Never tell me the odds',
        'roshi': 'Laugh',
        'oogway': 'Present',
        'sid': 'I choose life',
        'shifu': 'Level zero',
        'chunk': 'Chocolate eruption',
        'docholiday': 'Huckleberry',
        'kuzco': 'Credit',
        'majorpayne': 'Laugh',
    }

    @commands.command(aliases=tuple(filter(lambda name: name != 'yoda', defaults.keys())))
    async def yoda(self, ctx, *, query=None):
        await self.music.play(ctx, query if query else self.defaults[ctx.invoked_with])

    @commands.command()
    async def birthday(self, ctx):
        await ctx.send('HAPPY BIRTHDAY LIL REY!!', tts=True)


async def setup(bot):
    await bot.add_cog(SoundClipsCommands(bot))
