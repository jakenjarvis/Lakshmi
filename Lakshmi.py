#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import traceback

import discord
from discord.ext import commands

from MultilineBot import MultilineBot
from LakshmiHelpCommand import LakshmiHelpCommand
from LakshmiErrors import PermissionNotFoundException, ArgumentOutOfRangeException, SubcommandNotFoundException, UnsupportedSitesException, NotCallOfCthulhuInvestigatorException, CharacterNotFoundException

from contents.LakshmiBrainStorage import LakshmiBrainStorage

bot = MultilineBot(command_prefix=':', help_command=LakshmiHelpCommand())
bot.storage = LakshmiBrainStorage()

extensions = [
    'cogs.DiceBotCog',
    'cogs.GamesCog',
    'cogs.GreetingCog',
    'cogs.CallOfCthulhuCog'
]
for extension in extensions:
    bot.load_extension(extension)

@bot.event
async def on_ready():
    print("Lakshmi.on_ready()")
    print(discord.__version__)

@bot.event
async def on_command_error(context: commands.Context, error):
    if isinstance(error, ArgumentOutOfRangeException):
        character_message = bot.storage.get_character_message_for_argument_out_of_range_exception()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, PermissionNotFoundException):
        character_message = bot.storage.get_character_message_for_permission_not_found_exception()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, commands.MissingRequiredArgument):
        character_message = bot.storage.get_character_message_for_missing_required_argument()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, SubcommandNotFoundException):
        character_message = bot.storage.get_character_message_for_command_not_found()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, UnsupportedSitesException):
        character_message = bot.storage.get_character_message_for_unsupported_sites()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, NotCallOfCthulhuInvestigatorException):
        character_message = bot.storage.get_character_message_for_not_callofcthulhu_investigator()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, CharacterNotFoundException):
        character_message = bot.storage.get_character_message_for_character_not_found()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, commands.CommandNotFound):
        character_message = bot.storage.get_character_message_for_command_not_found()
        await context.send(f'{context.author.mention} {character_message}')

    else:
        original_error = getattr(error, "original", error)
        error_message = ''.join(traceback.TracebackException.from_exception(original_error).format())
        error_message = "```py\n" + error_message + "\n```"
        character_message = bot.storage.get_character_message_to_ask_the_developer_for_help()
        message = f'{context.author.mention}\n{character_message}\n{error_message}'
        await context.send(message)

token = bot.storage.environment.get_discord_token()
bot.run(token)
