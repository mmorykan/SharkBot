import os


class SoundClips:
    """
    Plays a file from the local filesystem
    Commands (all take one argument, the search query): 
        yoda, ewok, chewbacca, jabba, leia, hansolo, roshi,
        oogway, sid, shifu, chunk, docholiday, kuzco, majorpayne,
        birthday
    """
    
    @staticmethod
    def find_file(query, folder_name):
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
