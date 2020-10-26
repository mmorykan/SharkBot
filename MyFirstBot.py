import discord
from discord.ext import commands
import random
import os
import glob
import inspect
import emoji
from ffmpegPlay import FFmpegPCMAudio, PCMVolumeTransformer
from MyQueue import MusicPlayer
from HelpCommand import HelpInfo
from TextAlert import send_message
import giphy_client
from giphy_client.rest import ApiException
from pytube import YouTube
from youtubesearchpython import SearchVideos
import io


discord.opus.load_opus('/home/linuxbrew/.linuxbrew/Cellar/opus/1.3.1/lib/libopus.so')
# number of characters across one line is 79
bot = commands.Bot(command_prefix='$', description='The PS2 cheats sitting in your basement')
bot.remove_command('help')

DISCORD_TOKEN = os.getenv('DISCORD_API_TOKEN')
GIPHY_TOKEN = os.getenv('GIPHY_TOKEN')
HOME = os.getenv('HOME')
api_instance = giphy_client.DefaultApi()


class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gif(self, ctx, *, key='chonk'):
        gif_dict = {'monkey': 'https://media.giphy.com/media/l1KVboXQeiaX7FHgI/giphy.gif',
                    'quad': 'https://media.giphy.com/media/lD0OBtwl2Xxm0/giphy.gif',
                    'fountain': 'https://media.giphy.com/media/xTiTncVep2khPGhK1i/giphy.gif',
                    'chonk': 'https://media.giphy.com/media/G3773sSDJHHy0/giphy.gif',
                    'alien': 'https://media.giphy.com/media/RJddmVhFR04GisOuII/giphy.gif',
                    'roshi': 'https://media.giphy.com/media/H6Sqh74E5X7EY/giphy.gif',
                    'sweetie': 'https://media.giphy.com/media/Lq0h93752f6J9tijrh/giphy.gif',
                    'munchie': 'https://media.giphy.com/media/kI5yy4lcwnACQ/giphy.gif'}

        if key.lower().strip() in gif_dict:
            await ctx.send(gif_dict[key.lower().strip()])
        else:
            response = api_instance.gifs_search_get(GIPHY_TOKEN, key, limit=1)
            if response is None:
                sad = emoji.emojize(':sob:')
                await ctx.send(f'I Cannot find that gif {sad}{sad}')
            await ctx.send((response.data)[0].url)
       
    @commands.command(aliases=['shelbu', 'shelbutron', 'shelbs'])
    async def shelby(self, ctx):
        await ctx.send('https://media.giphy.com/media/w8wjiZVezPwNa/giphy.gif')

    @commands.command(aliases=['sweets', 'sweeter', 'banshee', 'sweetie'])
    async def sweety(self, ctx):
        await ctx.send('https://media.giphy.com/media/Lq0h93752f6J9tijrh/giphy.gif')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.message.author.mention}')

    @commands.command()
    async def random_number(self, ctx, lower_bound=1, upper_bound=1001):
        if lower_bound < upper_bound:
            await ctx.send(random.randrange(lower_bound, upper_bound))
        else:
            await ctx.send('Oh no! I can\'t do that!\nFirst argument has to be lower than second argument \n'
                           'Usage: $random_number <Lower Bound> <Upper Bound>')

    @commands.command()
    async def server(self, ctx):
        await ctx.send(f'{ctx.guild} is my favorite server!')

    @commands.command(aliases=['bill'])
    async def pumkinhed(self, ctx):
        face = emoji.emojize(':stuck_out_tongue_closed_eyes:')
        bill = str(bot.get_user(437456937735684097)).split('#')[0]
        await ctx.send(f'{bill} is mega big dumb {face}')

    @commands.command()
    async def info(self, ctx):
        happy = emoji.emojize(':smiley:')
        embed = discord.Embed(title='SharkBot', description='A friendly Shark.'
                                                            ' I play music from Youtube and sound clips from my soundboard.'
                                                            f' Try typing $help for a list of my commands {happy}',
                              color=0x0000CD)
        embed.add_field(name="Author",
                        value=bot.get_user(658765890334097429).mention,
                        inline=False)
        embed.add_field(name='Server Count', value=f"{len(bot.guilds)}", inline=False)
        embed.add_field(name='Invite',
                        value='https://discordapp.com/api/oauth2/authorize?client_id=662501433156960266&permissions=522304&scope=bot',
                        inline=False)

        await ctx.message.channel.send(embed=embed)


class Music(commands.Cog):
    """
    Don't need executable path on the raspberry pi
    Need a party time command for ravvessss
    """
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.currently_playing = ''


    @commands.command()
    async def play(self, ctx, *, url='angel wings avianna acid'):
        """Streams from a url. Does NOT download audio file"""
        self.currently_playing = url
        if not await self.ensure_voice(ctx):
            return

        # ffmpeg_options = {
        #     # 'before_options': ' -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        #     'options': '-vn'
        # }

        async with ctx.typing():
            search_results = SearchVideos(url, mode="dict", max_results = 5).result()
            print('search result:', search_results)
            result = search_results['search_result']
            if not result:
                sad = emoji.emojize(':sob:')
                return await ctx.send(f'I cannot find that song! {sad}')

            while result and result[0]['duration'] == 'LIVE':
                result.pop(0)

            if not result:
                sad = emoji.emojize(':sob:')
                return await ctx.send(f'I cannot find that song! {sad}')

            link = result[0]['link']
            print('link:', link)
            yt = YouTube(link)   # Get yt player config could not match pattern for song
            # JSON decode error unterminated string starting at line 1

            song = yt.streams.filter(only_audio=True).first()
            # player = await YTDLSource.from_url(ctx, url, loop=self.bot.loop, stream=True)

        correct_guild = self.get_correct_guild(ctx)
        try:
            # correct_guild.queue.put_nowait((correct_guild.play_next_queue_counter, player))
            data = {'song': song, 'requester': ctx.author.name, 'title': yt.title, 'duration': result[0]['duration'],'url': link}
            correct_guild.queue.put_nowait((correct_guild.play_next_queue_counter, data))
        except asyncio.QueueFull:
            await self.maxsized_queue(ctx)
            return

        correct_guild.play_next_queue_counter -= 1
        if correct_guild.current_song:
            await correct_guild.display_song_message(data['title'], data['requester'], data['duration'], data['url'])


    @commands.command()
    async def replay(self, ctx):
        if not await self.ensure_voice(ctx):
            return 

        correct_guild = self.get_correct_guild(ctx)
        if correct_guild.ctx.voice_client.is_playing():
            await correct_guild.replay()
        else:
            sad = emoji.emojize(':disappointed:')
            await ctx.send(f'No song to replay {sad}')


    @commands.command()
    async def shuffle(self, ctx):
        if not await self.ensure_voice(ctx):
            return 

        correct_guild = self.get_correct_guild(ctx)
        sad = emoji.emojize(':disappointed:')
        if correct_guild.queue.empty():
            await ctx.send(f'Queue is empty {sad}')
        else:
            await correct_guild.shuffle()

    @commands.command()
    async def now(self, ctx):
        if not await self.ensure_voice(ctx):
            return

        correct_guild = self.get_correct_guild(ctx)
        if correct_guild.ctx.voice_client.is_playing():
            await correct_guild.currently_playing()
        else:
            sad = emoji.emojize(':disappointed:')  
            await ctx.send(f'There is no song playing {sad}')

    def get_correct_guild(self, ctx):
        """Obtain the correct server"""

        try:
            correct_guild = self.players[ctx.guild.id]
        except KeyError:
            correct_guild = MusicPlayer(ctx)
            self.players[ctx.guild.id] = correct_guild

        return correct_guild

    @classmethod
    async def not_same_channel(cls, ctx):
        await ctx.send('Oh no! I\'m not in this channel!')

    async def maxsized_queue(self, ctx):
        correct_guild = self.get_correct_guild(ctx)
        await ctx.send(f'I cannot queue more than {correct_guild.queue.maxsize} songs')


    async def ensure_voice(self, ctx):
        flag = True
        if ctx.voice_client is not None:
            if ctx.author.voice:
                if ctx.voice_client.channel != ctx.author.voice.channel:
                    await self.cleanup(ctx.guild)
                    try:
                        await ctx.author.voice.channel.connect()
                    except:
                        pass
                else:
                    if ctx.voice_client.is_playing() and inspect.stack()[1][3] != 'add' and inspect.stack()[1][3] != 'play' and inspect.stack()[1][3] != 'now' and inspect.stack()[1][3] != 'shuffle' and inspect.stack()[1][3] != 'replay':
                        ctx.voice_client.stop()
            else:
                await self.not_same_channel(ctx)
                flag = False
        else:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await self.not_same_channel(ctx)
                flag = False

        return flag

    @commands.command()
    async def connect(self, ctx):
        await self.connect_helper(ctx)

    async def connect_helper(self, ctx):
        discord.opus.load_opus('/home/linuxbrew/.linuxbrew/Cellar/opus/1.3.1/lib/libopus.so')   # Dont need this line on the pi
        gameboy = SoundClips(bot)
        if ctx.voice_client is not None:
            if ctx.author.voice:
                if ctx.voice_client.channel != ctx.author.voice.channel:
                    await self.cleanup(ctx.guild)

                    try:
                        await ctx.author.voice.channel.connect()
                        await gameboy.on_join(ctx)
                    except:
                        print('couldnt join 1')
                else:
                    await ctx.send('Hey I\'m already connected')
            else:
                await ctx.send('I cannot be summoned outside of a voice channel')
        else:
            if ctx.author.voice:
                try:
                    await ctx.author.voice.channel.connect()
                    await gameboy.on_join(ctx)
                except:
                    print('Couldnt join 2')
            else:
                await ctx.send('I cannot be summoned outside of a voice channel')

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.voice_client is not None:
            if ctx.author.voice and ctx.voice_client.channel == ctx.author.voice.channel:
                await self.cleanup(ctx.guild)
            else:
                await self.not_same_channel(ctx)
        else:
            await ctx.send('My voice is not connected. Try using $connect or $play')

    
    @commands.command()
    async def add(self, ctx, *, url='angel wings avianna acid'):
        if not await self.ensure_voice(ctx):
            return

        ffmpeg_options = {
            # 'before_options': ' -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        correct_guild = self.get_correct_guild(ctx)
        async with ctx.typing():
            # source = await YTDLSource.from_url(ctx, url, loop=self.bot.loop, stream=True)
            search_results = SearchVideos(url, mode="dict", max_results = 5).result()
            print('search result:', search_results)
            result = search_results['search_result']
            if not result:
                sad = emoji.emojize(':sob:')
                return await ctx.send(f'I cannot find that song! {sad}')

            while result and result[0]['duration'] == 'LIVE':
                result.pop(0)

            if not result:
                sad = emoji.emojize(':sob:')
                return await ctx.send(f'I cannot find that song! {sad}')

            link = result[0]['link']
            print('link:', link)
            yt = YouTube(link)   # Get yt player config could not match pattern for song
            # JSON decode error unterminated string starting at line 1

            song = yt.streams.filter(only_audio=True).first()
            # player = await YTDLSource.from_url(ctx, url, loop=self.bot.loop, stream=True)

        try:
            data = {'song': song, 'requester': ctx.author.name, 'title': yt.title, 'duration': result[0]['duration'],'url': link}
            correct_guild.queue.put_nowait((correct_guild.add_queue_counter, data))
        except asyncio.QueueEmpty:
            await self.maxsized_queue(ctx)
            return

        correct_guild.add_queue_counter += 1
        if correct_guild.current_song:
            await correct_guild.display_song_message(data['title'], data['requester'], data['duration'], data['url'])


    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            await self.not_same_channel(ctx)
        else:
            if ctx.author.voice:
                if ctx.voice_client.channel != ctx.author.voice.channel:
                    await self.not_same_channel(ctx)
                else:
                    if ctx.voice_client.is_playing():
                        correct_guild = self.get_correct_guild(ctx)
                        if correct_guild.current_song:
                            current_song = correct_guild.current_song
                            ctx.voice_client.stop()
                            await correct_guild.display_song_message(current_song['title'], ctx.author.name, current_song['duration'], current_song['url'])
                        else:
                            ctx.voice_client.stop()
                    else:
                        await ctx.send('I was not playing anything')
            else:
                await self.not_same_channel(ctx)


    @commands.command(aliases=['stop'])
    async def pause(self, ctx):
        if ctx.voice_client is not None:
            if ctx.voice_client.is_playing():
                if ctx.author.voice and ctx.voice_client.channel == ctx.author.voice.channel:
                    ctx.voice_client.pause()
                else:
                    await self.not_same_channel(ctx)
            else:
                await ctx.send('I was not playing anything')
        else:
            await self.not_same_channel(ctx)


    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is not None:
            if ctx.voice_client.is_paused():
                if ctx.author.voice and ctx.voice_client.channel == ctx.author.voice.channel:
                    ctx.voice_client.resume()
                else:
                    await self.not_same_channel(ctx)
            else:
                await ctx.send('I was not paused')
        else:
            await self.not_same_channel(ctx)


    @commands.command()
    async def volume(self, ctx, volume: float=10.0):

        if ctx.voice_client is not None:
            if ctx.author.voice and ctx.voice_client.channel == ctx.author.voice.channel:
                if ctx.voice_client.is_playing():
                    if 0 <= volume <= 100:
                        ctx.voice_client.source.volume = volume / 100
                        await ctx.send(f'Changed volume to {volume}')
                    else:
                        await ctx.send('My volume level must be between 0 and 100')
                else:
                    await ctx.send('I am not playing anything yet!')
            else:
                await self.not_same_channel(ctx)
        else:
            await ctx.send('I am not connected to this channel. Try using $connect or $play from within a voice channel')


    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass
        try:
            del self.players[guild.id]
        except KeyError:
            pass


# All audio clips are downloaded and stored locally
class SoundClips(commands.Cog):
    """
    Plays a file from the local filesystem
    Don't need executable path on pi
    Make sure to use the bash command to find all files instead of hardcoding them in!!!!!!!
    """

    def __init__(self, bot):
        self.bot = bot


    async def find_files(self, ctx, query):
        folder_name = (inspect.stack()[1][3]).title()
        for filename in glob.glob(f'{os.sep}home{os.sep}ec2-user{os.sep}SoundClips{os.sep}{folder_name}{os.sep}*'): # This will be the path of the files on the pi
            if ''.join(query.lower().split()) in filename.lower()[filename.rfind(os.sep):]: 
                return filename

        await ctx.send('I don\'t have that quote' + emoji.emojize(':sob:'))
        return None

    @commands.command()
    async def yoda(self, ctx, *, query='Do or do not'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def ewok(self, ctx, *, query='Shout'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def chewbacca(self, ctx, *, query='Shout'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def jabba(self, ctx, *, query='Laugh'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def leia(self, ctx, *, query='Help me'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def hansolo(self, ctx, *, query='Never tell me the odds'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def roshi(self, ctx, *, query='Laugh'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def oogway(self, ctx, *, query='Present'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def sid(self, ctx, *, query='I choose life'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def shifu(self, ctx, *, query='Level zero'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def chunk(self, ctx, *, query='Chocolate eruption'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def docholiday(self, ctx, *, query='Huckleberry'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def kuzco(self, ctx, *, query='credit'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def majorpayne(self, ctx, *, query='Laugh'):

        await self.play_quotes(ctx, await self.find_files(ctx, query))

    @commands.command()
    async def birthday(self, ctx):

        await ctx.send('HAPPY BIRTHDAY!!', tts=True)

    @classmethod
    async def on_join(cls, ctx):
        source = '/home/ec2-user/SoundClips/GameboyStartup.m4a'    #Path to file on Raspberry pi
        player = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(source, executable='/home/linuxbrew/.linuxbrew/Cellar/ffmpeg/4.3_2/bin/ffmpeg'))

        ctx.voice_client.play(player)

    @classmethod
    async def play_quotes(cls, ctx, filename):
        temp = Music(bot)
        if not await temp.ensure_voice(ctx) or filename is None:
            return

        try:
            if ctx.voice_client.is_paused():
                temp.cleanup(temp.get_correct_guild(ctx))
        except:
            pass

        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(filename, executable='/home/linuxbrew/.linuxbrew/Cellar/ffmpeg/4.3_2/bin/ffmpeg'))
        ctx.voice_client.play(source)


@bot.event
async def on_member_join(member):

    for channel in member.guild.channels:
        if channel.name == 'general':
            exclaim = emoji.emojize(':exclamation:')
            await channel.send(f'Welcome {member.name}{exclaim}')
            break

@bot.event
async def on_guild_join(guild):
    try:
        send_message(f'SharkBot has joined {guild}!')
    except:
        pass


@bot.event
async def on_member_ban(guild, user):
    for channel in guild.channels:
        if channel.name == 'general':
            await channel.send(f'Ha! What a loser {user.name}')
            break

##### Add the guild join event and text me when it happens #####
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    elif message.content.strip().lower() == '$help':
        temp = HelpInfo()
        await temp.helper(message)

    await bot.process_commands(message)             # Need this line to process other commands


# Greets everyone in the server
@bot.event
async def on_ready():

    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.add_cog(Miscellaneous(bot))
bot.add_cog(Music(bot))
bot.add_cog(SoundClips(bot))
bot.run(DISCORD_TOKEN)
