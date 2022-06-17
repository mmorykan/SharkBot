import os
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from Music import Music


class SoundClips():
    """
    Plays a file from the local filesystem
    Commands (all take one argument, the search query): 
        yoda, ewok, chewbacca, jabba, leia, hansolo, roshi,
        oogway, sid, shifu, chunk, docholiday, kuzco, majorpayne,
        birthday
    """

    def __init__(self):
        self.music = Music()

    async def play(self, ctx, query, folder_name):
        await self.play_quotes(ctx, await self.find_file(query, folder_name))

    async def find_file(self, query, folder_name):
        """
        Walks through the SoundClips directory looking for the file closest to the search query.
        :param query: The search query to get matched to a name of a file
        :type query: str
        :param folder_name: The name of the directory within SoundClips to walk through
        :type folder_name: str
        :returns: The path to the queried audio file if found
        :rtype: str
        """

        folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SoundClips', folder_name)
        files = os.listdir(folder_path)
        for filename in files:
            clip_name = ''.join(query.lower().split())
            if clip_name in filename.lower():
                return os.path.join(folder_path, filename)

        return os.path.join(folder_path, files[0])

    async def play_quotes(self, ctx, file_):
        """
        Play the quote if found, making sure there is a voice client connected. Defaults to first file in folder.
        :param file_: The file to play. Typically a .wav file.
        :type filename: str
        """

        await self.music.connect(ctx)
        source = PCMVolumeTransformer(FFmpegPCMAudio(file_), self.music.get_correct_guild(ctx).volume)
        setattr(source, 'data', {'requester': ctx.author.name, 'title': file_.rsplit(os.sep)[-1], 'duration': 0, 'webpage_url': None})
        await self.music.add_to_queue(ctx, source, ['Queued in front: ', 'Queued by: '], True)
