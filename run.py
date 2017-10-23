#!/usr/bin/env python3

# Brainfug by T3CHNOLOG1C
# license: Apache License 2.0
# https://github.com/T3CHNOLOG1C/Brainfug
# Based off of Kurisu
# https://github.com/ihaveamac/Kurisu

# import dependencies
import asyncio
import copy
import configparser
import datetime
import imp
import json
import os
import re
import sys
import traceback
import discord
from discord.ext import commands


description = """
Brainfug, a bot for interpreting Brainf*ck code!
"""

# sets working directory to bot's folder
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# read config for token
config = configparser.ConfigParser()
config.read("config.ini")

prefix = ['$']
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None)

# http://stackoverflow.com/questions/3411771/multiple-character-replace-with-python
chars = "\\`*_<>#@:~"


def escape_name(name):
    name = str(name)
    for c in chars:
        if c in name:
            name = name.replace(c, "\\" + c)
    return name.replace("@", "@\u200b")  # prevent mentions


bot.escape_name = escape_name

bot.all_ready = False
bot._is_all_ready = asyncio.Event(loop=bot.loop)
async def wait_until_all_ready():
    """Wait until the entire bot is ready."""
    await bot._is_all_ready.wait()
bot.wait_until_all_ready = wait_until_all_ready

@bot.event
async def on_ready():
    # this bot should only ever be in one server anyway
    for server in bot.servers:
        bot.server = server
        if bot.all_ready:
            break

        print("{} has started! {} has {:,} members!".format(bot.user.name, server.name, server.member_count))


        bot.all_ready = True
        bot._is_all_ready.set()

        break

# loads extensions
addons = [
    'addons.bf',
]

failed_addons = []

for extension in addons:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print('{} failed to load.\n{}: {}'.format(extension, type(e).__name__, e))
        failed_addons.append([extension, type(e).__name__, e])

# Execute
print('Bot directory: ', dir_path)
bot.run(config['Main']['token'])
