from discord.ext import commands
import giphy_client
import emoji
import random
import discord


class Miscellaneous(commands.Cog):
    """
    Commands:
    - gif <query>
    - shelby
    - sweety
    - hello
    - random_number <lower> <upper>
    - server
    - ruv
    - info
    """

    def __init__(self, bot, token):
        """Saves the Giphy credentials in order to send gifs"""

        self.bot = bot
        self.giphy_token = token

    @commands.command()
    async def gif(self, ctx, *, key='chonk'):
        """
        Sends a gif from giphy based on user search query. Also provides some hardcoded specialities as well.
        :param key: The search query for a gif
        :type key: str
        """

        # Hardcoded gif favorites
        gif_dict = {'monkey': 'https://media.giphy.com/media/l1KVboXQeiaX7FHgI/giphy.gif',
                    'quad': 'https://media.giphy.com/media/lD0OBtwl2Xxm0/giphy.gif',
                    'fountain': 'https://media.giphy.com/media/xTiTncVep2khPGhK1i/giphy.gif',
                    'chonk': 'https://media.giphy.com/media/G3773sSDJHHy0/giphy.gif',
                    'alien': 'https://media.giphy.com/media/RJddmVhFR04GisOuII/giphy.gif',
                    'roshi': 'https://media.giphy.com/media/H6Sqh74E5X7EY/giphy.gif',
                    'sweetie': 'https://media.giphy.com/media/Lq0h93752f6J9tijrh/giphy.gif',
                    'munchie': 'https://media.giphy.com/media/kI5yy4lcwnACQ/giphy.gif'}

        url = gif_dict.get(key.lower().strip())
        if url:
            await ctx.send(url)
        else:
            api_instance = giphy_client.DefaultApi()  # Create giphy client object
            response = api_instance.gifs_search_get(self.giphy_token, key, limit=1)  # Search using the query
            data = response.data
            sad = emoji.emojize(':sob:')
            await ctx.send(data[0].url) if data else await ctx.send(f'I Cannot find that gif {sad}{sad}')
       
    @commands.command(aliases=['shelbu', 'shelbutron', 'shelbs'])
    async def shelby(self, ctx):
        """Sends a gif of a husky"""

        await ctx.send('https://media.giphy.com/media/w8wjiZVezPwNa/giphy.gif')

    @commands.command(aliases=['sweets', 'sweeter', 'banshee', 'sweetie'])
    async def sweety(self, ctx):
        """Sends a gif of a loud cat"""

        await ctx.send('https://media.giphy.com/media/Lq0h93752f6J9tijrh/giphy.gif')

    @commands.command()
    async def hello(self, ctx):
        """Used for debugging, mainly to see if SharkBot is responding. Similar to ping command."""

        await ctx.send(f'Hello {ctx.message.author.mention}')

    @commands.command()
    async def random_number(self, ctx, lower_bound=1, upper_bound=1001):
        """
        Generates and sends a random number based on lower and upper bounds
        :param lower_bound: The lower bound of a random integer
        :type lower_bound: int, optional
        :param upper_bound: The upper bound of a random integer
        :type upper_bound: int, optional
        """

        if lower_bound < upper_bound:
            await ctx.send(random.randrange(lower_bound, upper_bound))
        else:
            await ctx.send('Oh no! I can\'t do that!\nFirst argument has to be lower than second argument \n'
                           'Usage: $random_number <Lower Bound> <Upper Bound>')

    @commands.command()
    async def server(self, ctx):
        """Sends a message saying the current server is the favorite server"""

        await ctx.send(f'{ctx.guild} is my favorite server!')

    @commands.command(aliases=['aruv', 'whale'])
    async def ruv(self, ctx):
        """Gets a specific user and displays a message about them. Only works in certain guilds"""

        face = emoji.emojize(':stuck_out_tongue_closed_eyes:')
        ruv = str(self.bot.get_user(139187096366743552)).split('#')[0]
        await ctx.send(f'{ruv} is mega big dumb {face}')

    @commands.command()
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
