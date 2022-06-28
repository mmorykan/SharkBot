from discord.ext.commands import Cog
from Music import Music


class Audio(Cog):

    def __init__(self):
        self.music = Music()

    async def cleanup(self, ctx):
        await ctx.voice_client.disconnect()
        del self.music.players[ctx.guild.id]
