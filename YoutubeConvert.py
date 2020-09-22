import youtube_dl
import discord
import asyncio
from functools import partial

'''
Specifics for youtube_dl formatting.
If using subprocess to download Youtube audio instead of stream, use '-f bestaudio+worstvideo/best'
'''

ytdl_format_options = {
    'format': 'bestaudio/best',  # Cannot do bestaudio+worstvideo/best because youtube_dl in Python requires one url
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',    # Auto means you can obtain Youtube audio file through key words instead of url
    'source_address': '0.0.0.0'  # Bind to ipv4 since ipv6 may cause problems.
                                 # May have to bind this to my own IP in the future.
}

# before_options is crucial. Without it, the youtube url will expire during the stream and audio will quit
ffmpeg_options = {
    'before_options': ' -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5, requester):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.requester = requester


    @classmethod
    async def from_url(cls, ctx, url, *, loop=None, stream=False):
        """This gets a playable audio source to stream from Youtube"""

        loop = loop or asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        except:
            return

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        
        # To access duration of videos, use data['duration']
        return cls(discord.FFmpegPCMAudio(
            filename,
            before_options=ffmpeg_options['before_options'],
            options=ffmpeg_options['options'],
            executable='/home/linuxbrew/.linuxbrew/Cellar/ffmpeg/4.3_2/bin/ffmpeg'),
            data=data,
            requester=ctx.author.name)


    # def clone(ytdl_object):
    #     return YTDLSource(self.source, self.data, self.volume, self.requester)
 
