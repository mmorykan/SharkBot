from discord import PCMVolumeTransformer


class AudioSource(PCMVolumeTransformer):
    """
    :param source: Discord audio source that can be streamed through voice client
    :type source: discord.FFmpegPCMAudio
    :param data: Recorded information about the source such as artist and url
    :type data: dict
    :param volume: The volume for the audio source. Only available because this inherits from discord.PCMVolumeTransformer
    :type volume: float, optional
    """

    def __init__(self, source, data, volume):
        super().__init__(source, volume)
        self.data = data
