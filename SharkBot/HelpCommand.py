import discord
from discord.ext import commands

class HelpInfo(commands.Cog):
    """
    Wrapper for the help command so that the help function can be accessed through a Cog.
    """

    @commands.command()
    async def help(self, ctx):
        """One discord Embed with one field per command. Color is dark blue."""
        embed = discord.Embed(title='SharkBot', description='Here is a list of my commands',
                                color=0x0000CD)

        embed.add_field(name='$hello', value='Greets the user', inline=False)
        embed.add_field(name='$gif <argument>',
                        value='Displays a gif based on key word search or one of the following arguments: monkey, quad, fountain, chonk, alien, roshi, sweetie, munchie',
                        inline=False)
        embed.add_field(name='$shelby', value='A greeting from Shelby', inline=False)
        embed.add_field(name='$sweety', value='A greeting from Sweety', inline=False)
        embed.add_field(name='$server', value='Displays the server\'s name', inline=False)
        embed.add_field(name='$birthday', value='Sends a happy birthday message', inline=False)
        embed.add_field(name='$random_number <Lower Bound> <Upper Bound>',
                        value='Random number generator: \n<Lower Bound> Default: 0 \n<Upper Bound> Default: 1001',
                        inline=False)
        embed.add_field(name='$connect', value='Connects SharkBot to the current voice channel', inline=False)
        embed.add_field(name='$disconnect', value='Disconnects SharkBot from the current voice channel', inline=False)
        embed.add_field(name='$play', value='Streams audio from a youtube video', inline=False)
        embed.add_field(name='$pause', value='Pauses the audio currently playing', inline=False)
        embed.add_field(name='$resume', value='Resumes the audio currently paused', inline=False)
        embed.add_field(name='$add', value='Adds a song to a queue and plays the first one immediately', inline=False)
        embed.add_field(name='$skip', value='Skips the song currently being played', inline=False)
        embed.add_field(name='$replay', value='Replays the current song', inline=False)
        embed.add_field(name='$shuffle', value='Shuffles the queue', inline=False)
        embed.add_field(name='$now', value='Gets the currently playing song', inline=False)
        embed.add_field(name='$show', value='Displays a message for each song in the queue in the correct order', inline=False)
        embed.add_field(name='$yoda', value='Play a quote from Yoda: \n'
                                            ' - 900 years old \n'
                                            ' - do or do not \n'
                                            ' - size matters not \n'
                                            ' - unlearn what you have learned \n'
                                            ' - laugh \n'
                                            ' - cannot teach \n'
                                            ' - learn control \n'
                                            ' - reckless',
                        inline=False)
        embed.add_field(name='$chewbacca <quote>', value='Play a shout from Chewbacca: \n'
                                                    ' - shout',
                        inline=False)
        embed.add_field(name='$ewok <quote>', value='Play a shout or a song from an ewok: \n'
                                            ' - shout \n'
                                            ' - sing',
                        inline=False)
        embed.add_field(name='$jabba <quote>', value='Play a laugh from Jabba the Hutt: \n'
                                                ' - laugh',
                        inline=False)
        embed.add_field(name='$leia <quote>', value='Play the famous \"help me\" message from Leia: \n'
                                            ' - help',
                        inline=False)
        embed.add_field(name='$hansolo <quote>', value='Play a famous Han Solo quote: \n'
                                                ' - never tell me the odds',
                        inline=False)
        embed.add_field(name='$roshi <quote>', value='Play Master Roshi\'s laugh: \n'
                                                ' - laugh',
                        inline=False)
        embed.add_field(name='$oogway <quote>', value='Plays a quote from Master Oogway: \n'
                                                ' - Your mind is like water \n'
                                                ' - Present \n'
                                                ' - One meets destiny \n'
                                                ' - There is no news \n'
                                                ' - My time has come \n'
                                                ' - I don\'t know',
                        inline=False)
        embed.add_field(name='$shifu <quote>', value='Play a quote from Master Shifu: \n'
                                                ' - Level zero',
                        inline=False)
        embed.add_field(name='$sid <quote>', value='Play a quote from Sid the sloth: \n'
                                            ' - I choose life \n'
                                            ' - Lord of the flame',
                        inline=False)
        embed.add_field(name='$chunk <quote>', value='Play a quote from Chunk: \n'
                                                ' - Chocolate eruption \n'
                                                ' - Summer camp for fat kids',
                        inline=False)
        embed.add_field(name='$docholiday <quote>', value='Play a quote from Doc Holiday: \n'
                                                    ' - Huckleberry \n'
                                                    ' - I hate him',
                        inline=False)
        embed.add_field(name='$kuzco <quote>', value='Play a quote from Emperor Kuzco: \n'
                                                ' - Too much credit \n'
                                                ' - Make deals with peasants \n'
                                                ' - You threw off my groove \n'
                                                ' - Favorite village man \n'
                                                ' - Whiny peasant',
                        inline=False)
        embed.add_field(name='$majorpayne <quote>', value='Play Major Payne\'s laugh: \n'
                                                    ' - Laugh',
                        inline=False)
        embed.add_field(name='$ruv', value='Displays a message about Ruv', inline=False)
        embed.add_field(name='$info', value='Displays information about Sharkbot', inline=False)
        embed.add_field(name='$help', value='Displays all available SharkBot commands', inline=False)

        await ctx.send(embed=embed)
