import os
from discord import FFmpegPCMAudio
from AudioSource import AudioSource


class SoundClips(AudioSource):
    """
    Plays a file from the local filesystem
    Commands (all take one argument, the search query): 
        yoda, ewok, chewbacca, jabba, leia, hansolo, roshi,
        oogway, sid, shifu, chunk, docholiday, kuzco, majorpayne,
        birthday
    """

    @classmethod
    async def get_source(cls, ctx, query, volume):
        """
        Walks through the SoundClips directory looking for the file closest to the search query.
        :param query: The search query to get matched to a name of a file
        :type query: str
        :param folder_name: The name of the directory within SoundClips to walk through
        :type folder_name: str
        :returns: The path to the queried audio file if found
        :rtype: str
        """

        folder_name = ctx.invoked_with.capitalize()
        folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SoundClips', folder_name)
        files = os.listdir(folder_path)
        file_ = os.path.join(folder_path, files[0])
        for filename in files:
            clip_name = ''.join(query.lower().split())
            if clip_name in filename.lower():
                file_ = os.path.join(folder_path, filename)

        return cls(FFmpegPCMAudio(file_), 
               {'requester': ctx.author.name, 'title': file_.rsplit(os.sep)[-1], 'duration': 0, 'webpage_url': None, 'query': query}, 
               volume)
