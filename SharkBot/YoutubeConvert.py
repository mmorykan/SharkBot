import yt_dlp
from datetime import timedelta
from discord import FFmpegPCMAudio
from AudioSource import AudioSource


# Set up formatting options for optimal streaming
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
    'default_search': 'auto',    # Auto means you can obtain Youtube audio file through search queries instead of url
    'source_address': '0.0.0.0'  # Bind to ipv4 since ipv6 may cause problems.                             
}

# before_options is crucial. Without it, the youtube url will expire during the stream and audio will quit
ffmpeg_options = {
    'before_options': ' -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(AudioSource):
    """
    Creates the player object to be stored in the queue.
    Subclass of discord.PCMVolumeTransformer in order to access volume attribute.
    Records downloaded information about the song.
    """        
        
    @classmethod
    async def from_url(cls, ctx, url, volume):
        """
        Gets a playable audio source to stream from Youtube.
        :param url: Search query to send to Youtube
        :type url: str
        :param volume: The volume for the audio source.
        :type volume: float
        :returns: An object containing the audio source, ffmpeg options for playback, and recorded data
        :rtype: YTDLSource
        """

        data = await ctx.bot.loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if 'entries' in data:  # Enter if url is a search query instead of a url
            while not data['entries']:  # entries field contains the url. Sometimes entries list is empty. Loop until not empty
                data = await ctx.bot.loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            data = data['entries'][0]  # Gets first song

        return cls(FFmpegPCMAudio(
            data['url'],
            before_options=ffmpeg_options['before_options'],
            options=ffmpeg_options['options']),
            data=cls.format_data(data, ctx.author.name),
            volume=volume)

    @staticmethod
    def format_data(data, requester):
        """
        Gets all the necessary data from the extracted data from the url
        :param data: The extracted data from the url, containing information about everything on the Youtube url's page
        :type data: dict
        :param requester: The user who requested this song
        :type requester: str
        :returns: The necessary information from the url's extracted information
        :rtype: dict
        """

        return {
            'duration': timedelta(seconds=data.get('duration')),  # duration is initially in seconds
            'description': data.get('description'),
            'categories': data.get('categories'),
            'channel_url': data.get('channel_url'),
            'webpage_url': data.get('webpage_url'),
            'upload_date': data.get('upload_date'),
            'view_count': data.get('view_count'),
            'like_count': data.get('like_count'),
            'dislike_count': data.get('dislike_count'),
            'average_rating': data.get('average_rating'),
            'title': data.get('title'),
            'url': data.get('url'),
            'requester': requester
        }
