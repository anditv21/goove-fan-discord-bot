import sys

sys.dont_write_bytecode = True
import asyncio
import os
import platform
from datetime import datetime
from urllib.parse import quote

import discord
from colorama import Fore
from discord.ext import commands, tasks

from helpers.config import get_config_value
from helpers.general import (clear_console, print_failure_message,
                             print_success_message)


loaded = 0
allcogs = 0

token = get_config_value('token')

class Bot(commands.Bot):
    def __init__(self, *, intents: discord.Intents):

        super().__init__(command_prefix=commands.when_mentioned_or("$$"), intents=intents)

    async def setup_hook(self):
        global loaded, allcogs
        clear_console()
        for filepath in os.listdir('cogs'):
            for filename in os.listdir(f'cogs/{filepath}'):
                if filename.endswith('.py'):
                    filename = filename.replace('.py', '')
                    allcogs += 1
                    try:
                        await bot.load_extension(f'cogs.{filepath}.{filename}')
                        print_success_message(f'Loaded cogs.{filepath}.{filename}')
                        loaded += 1
                    except Exception as error:
                        print_failure_message(f'Failed to load cogs.{filepath}.{filename}: {error}')

        await self.tree.sync()


intents = discord.Intents.default()
intents.members = True
bot = Bot(intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle)

    print_success_message(f'Loaded [{loaded}/{allcogs}] cogs')

    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="anditv.dev"),)
    print_success_message(f'has connected as {bot.user} via discord.py {discord.__version__}')




bot.run(token=token, log_level=40)
