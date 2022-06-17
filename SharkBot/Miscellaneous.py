import giphy_client
import emoji
import random
import discord


class Miscellaneous:

    def __init__(self, bot, token):
        """Saves the Giphy credentials in order to send gifs"""

        self.bot = bot
        self.giphy_token = token

    async def gif(self, ctx, key):
        """
        Sends a gif from giphy based on user search query. Also provides some hardcoded specialities as well.
        :param key: The search query for a gif
        :type key: str
        """

        # gif favorites
        gif_dict = {'monkey': 'l1KVboXQeiaX7FHgI',
                    'quad': 'lD0OBtwl2Xxm0',
                    'fountain': 'xTiTncVep2khPGhK1i',
                    'chonk': 'G3773sSDJHHy0',
                    'alien': 'RJddmVhFR04GisOuII',
                    'roshi': 'H6Sqh74E5X7EY',
                    'sweetie': 'Lq0h93752f6J9tijrh',
                    'munchie': 'kI5yy4lcwnACQ',}

        id_ = gif_dict.get(key.lower().strip())
        if id_:
            await self.send_gif(ctx, id_)
        else:
            api_instance = giphy_client.DefaultApi()  # Create giphy client object
            data = api_instance.gifs_search_get(self.giphy_token, key, limit=1).data  # Search using the query
            sad = emoji.emojize(':sob:')
            id_ = (await self.send_gif(ctx, data[0].id)) if data else (await ctx.send(f'I Cannot find that gif {sad}{sad}'))
    
    async def send_gif(self, ctx, id_):
        """"Sends a gif based on the id"""

        await ctx.send(f'https://media.giphy.com/media/{id_}/giphy.gif')

    async def random_number(self, ctx, lower_bound=1, upper_bound=1001):
        """
        Generates and sends a random number based on lower and upper bounds
        :param lower_bound: The lower bound of a random integer
        :type lower_bound: int, optional
        :param upper_bound: The upper bound of a random integer
        :type upper_bound: int, optional
        """

        if lower_bound < upper_bound:
            msg = random.randrange(lower_bound, upper_bound)
        else:
            msg = 'Oh no! I can\'t do that!\nFirst argument has to be lower than second argument \n'
            'Usage: $random_number <Lower Bound> <Upper Bound>'
        
        await ctx.send(msg)

    async def ruv(self, ctx):
        """Gets a specific user and displays a message about them. Only works in certain guilds"""

        face = emoji.emojize(':stuck_out_tongue_closed_eyes:')
        ruv = str(self.bot.get_user(139187096366743552)).split('#')[0]
        await ctx.send(f'{ruv} is mega big dumb {face}')

    async def info(self, ctx):
        """Display name of bot, author of bot, server count of bot, and the invite link for the bot"""

        happy = emoji.emojize(':smiley:')
        embed = discord.Embed(title='SharkBot', description='A friendly Shark.'
                                                            ' I play music from Youtube and sound clips from my soundboard.'
                                                            f' Try typing $help for a list of my commands {happy}',
                              color=0x0000CD)
        # embed.add_field(name="Author",
        #                 value=self.bot.get_user(658765890334097429).mention,
        #                 inline=False)
        embed.add_field(name='Server Count', value=f"{len(self.bot.guilds)}", inline=False)
        embed.add_field(name='Invite',
                        value='https://discordapp.com/api/oauth2/authorize?client_id=662501433156960266&permissions=522304&scope=bot',
                        inline=False)

        await ctx.message.channel.send(embed=embed)
