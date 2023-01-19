from discord.ext.commands import Cog
from Music import Music


class Audio(Cog):

    music = Music()

    async def cleanup(self, ctx):
        await ctx.voice_client.disconnect()
        del self.music.players[ctx.guild.id]


async def setup(bot):
    await bot.add_cog(Audio(bot))