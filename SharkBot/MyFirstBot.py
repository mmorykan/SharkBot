#!/usr/bin/env python3
import os
from dotenv import load_dotenv, find_dotenv
import emoji
import discord
import asyncio
from discord.ext import commands
from TextAlert import send_message

# Create the bot and remove default help command
bot = commands.Bot(command_prefix='$', help_command=None, description='The PS2 cheats sitting in your basement', intents=discord.Intents.all())

async def load_extensions():
    for filename in os.listdir(os.path.join(os.getcwd(), 'SharkBot', 'Commands')):
        if filename.endswith(".py"):
            await bot.load_extension(f"Commands.{filename[:-3]}")

@bot.event
async def on_reaction_remove(reaction, user):
    """
    When a reaction is removed, SharkBot is notified.
    :param reaction: The reaction that was removed
    :type reaction: discord.Reaction
    :param user: The user who removed the reaction
    :type user: discord.Member
    """

    await reaction.message.channel.send(emoji.emojize(':sob:') * 2)


@bot.event
async def on_member_join(member):
    """
    Welcome a new member.
    :param member: The member who just join the guild
    :type member: discord.Member
    """

    for channel in member.guild.channels:
        if channel.name == 'general':
            exclaim = emoji.emojize(':exclamation:')
            await channel.send(f'Welcome {member.name.mention}{exclaim}')
            break


@bot.event
async def on_member_ban(guild, user):
    """
    Send a message whenever a user is banned from a guild.
    :param guild: The guild that the user got banned from
    :type guild: discord.Guild
    :param user: The user that got banned
    :type user: discord.User
    """

    for channel in guild.channels:
        if channel.name == 'general':
            await channel.send(f'Ha! What a loser {user.name.mention}')
            break


@bot.event
async def on_guild_join(guild):
    """
    Texts my cell phone when SharkBot is invited into a new guild.
    :param guild: The guild that SharkBot was invited to
    :type guild: discord.Guild
    """
    try:
        send_message(f'SharkBot has joined {guild}!')
    except:
        pass


# @bot.event
# async def on_ready():
#     """First function to run when SharkBot starts up"""

#     print('Logged in as')
#     print(bot.user.name)
#     print(bot.user.id)
#     print('------')

if __name__ == '__main__':
    asyncio.run(load_extensions())
    load_dotenv(find_dotenv())
    DISCORD_TOKEN = os.getenv('DISCORD_API_TOKEN')
    bot.run(DISCORD_TOKEN)
