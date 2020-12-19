from discord.ext import commands
from Music import Music
import os
import discord


class SoundClips(commands.Cog):
    """
    Plays a file from the local filesystem
    Commands (all take one argument, the search query): 
        yoda, ewok, chewbacca, jabba, leia, hansolo, roshi,
        oogway, sid, shifu, chunk, docholiday, kuzco, majorpayne,
        birthday
    """

    def __init__(self, bot):
        self.bot = bot

    async def find_files(self, ctx, query, folder_name):
        """
        Walks through the SoundClips directory looking for the file closest to the search query.
        :param query: The search query to get matched to a name of a file
        :type query: str
        :param folder_name: The name of the directory within SoundClips to walk through
        :type folder_name: str
        :returns: The path to the queried audio file if found
        :rtype: str or None
        """

        folder_path = '../SoundClips/' + folder_name
        for filename in os.listdir(folder_path):
            clip_name = ''.join(query.lower().split())
            if clip_name in filename.lower():
                return folder_path + '/' + filename


    @commands.command()
    async def yoda(self, ctx, *, query='Do or do not'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Yoda'))


    @commands.command()
    async def ewok(self, ctx, *, query='Shout'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Ewok'))


    @commands.command()
    async def chewbacca(self, ctx, *, query='Shout'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Chewbacca'))


    @commands.command()
    async def jabba(self, ctx, *, query='Laugh'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Jabba'))


    @commands.command()
    async def leia(self, ctx, *, query='Help me'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Leia'))


    @commands.command()
    async def hansolo(self, ctx, *, query='Never tell me the odds'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Hansolo'))


    @commands.command()
    async def roshi(self, ctx, *, query='Laugh'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Roshi'))


    @commands.command()
    async def oogway(self, ctx, *, query='Present'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Oogway'))


    @commands.command()
    async def sid(self, ctx, *, query='I choose life'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Sid'))


    @commands.command()
    async def shifu(self, ctx, *, query='Level zero'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Shifu'))


    @commands.command()
    async def chunk(self, ctx, *, query='Chocolate eruption'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Chunk'))


    @commands.command()
    async def docholiday(self, ctx, *, query='Huckleberry'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Docholiday'))


    @commands.command()
    async def kuzco(self, ctx, *, query='credit'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Kuzco'))


    @commands.command()
    async def majorpayne(self, ctx, *, query='Laugh'):
        await self.play_quotes(ctx, await self.find_files(ctx, query, 'Majorpayne'))

    @commands.command()
    async def birthday(self, ctx):
        await ctx.send('HAPPY BIRTHDAY!!', tts=True)

    async def play_quotes(self, ctx, filename):
        """
        Play the quote if found, makeing sure there is a voice client connected.
        :param filename: The name of the file to play. Typically a .mp3 file.
        :type filename: str or None
        """

        music = Music(self.bot)
        if await music.ensure_voice(ctx) and filename:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename), volume=0.5)
            ctx.voice_client.play(source)
