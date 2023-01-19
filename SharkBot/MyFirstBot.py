#!/usr/bin/env python3
import os
from dotenv import load_dotenv, find_dotenv
import discord
import asyncio
from discord.ext import commands

# Create the bot and remove default help command
bot = commands.Bot(command_prefix='$', help_command=None, description='The PS2 cheats sitting in your basement', intents=discord.Intents.all())

async def load_extensions():
    load_dotenv(find_dotenv())
    for filename in os.listdir(os.path.join(os.getcwd(), 'SharkBot', 'Commands')):
        if filename.endswith(".py"):
            await bot.load_extension(f"Commands.{filename[:-3]}")


if __name__ == '__main__':
    asyncio.run(load_extensions())
    bot.run(os.getenv('DISCORD_API_TOKEN'))
