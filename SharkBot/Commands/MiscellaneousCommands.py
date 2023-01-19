import os
from discord.ext import commands
from Miscellaneous import Miscellaneous


class MiscellaneousCommands(commands.Cog):
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
        self.misc = Miscellaneous(bot, token)

    @commands.command()
    async def gif(self, ctx, *, key='chonk'):
        await self.misc.gif(ctx, key)

    @commands.command(aliases=['shelbu', 'shelbutron', 'shelbs'])
    async def shelby(self, ctx):
        await self.misc.send_gif(ctx, 'w8wjiZVezPwNa')

    @commands.command(aliases=['sweets', 'sweeter', 'banshee', 'sweetie'])
    async def sweety(self, ctx):
        await self.misc.send_gif(ctx, 'Lq0h93752f6J9tijrh')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.message.author.mention}')

    @commands.command()
    async def random_number(self, ctx, lower_bound=1, upper_bound=1001):
        await self.misc.random_number(ctx, lower_bound, upper_bound)

    @commands.command()
    async def server(self, ctx):
        await ctx.send(f'{ctx.guild} is my favorite server!')

    @commands.command(aliases=['aruv', 'whale'])
    async def ruv(self, ctx):
        await self.misc.ruv(ctx)

    @commands.command()
    async def info(self, ctx):
        await self.misc.info(ctx)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.misc.send_guild_join_msg(guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.misc.send_member_join_msg(member)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.misc.send_on_ready_msg()


async def setup(bot):
    GIPHY_TOKEN = os.getenv('GIPHY_TOKEN')
    await bot.add_cog(MiscellaneousCommands(bot, GIPHY_TOKEN))
