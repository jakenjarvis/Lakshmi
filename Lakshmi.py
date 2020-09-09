#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import traceback

import discord
from discord.ext import commands

from MultilineBot import MultilineBot
from LakshmiHelpCommand import LakshmiHelpCommand
import LakshmiErrors

from contents.LakshmiBrainStorage import LakshmiBrainStorage

bot = MultilineBot(command_prefix=';', help_command=LakshmiHelpCommand())
bot.storage = LakshmiBrainStorage(bot)

extensions = [
    'cogs.DiceBotCog',
    'cogs.GamesCog',
    'cogs.GreetingCog',
    'cogs.CallOfCthulhuCog',
    'cogs.ShortcutCallOfCthulhuCog',
]
for extension in extensions:
    bot.load_extension(extension)

@bot.event
async def on_ready():
    print("Lakshmi.on_ready()")
    print(discord.__version__)

@bot.event
async def on_command_error(context: commands.Context, error):
    if isinstance(error, LakshmiErrors.ArgumentOutOfRangeException):
        character_message = bot.storage.lexicon.get_character_message_for_argument_out_of_range_exception()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, LakshmiErrors.PermissionNotFoundException):
        character_message = bot.storage.lexicon.get_character_message_for_permission_not_found_exception()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, commands.MissingRequiredArgument):
        character_message = bot.storage.lexicon.get_character_message_for_missing_required_argument()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, LakshmiErrors.SubcommandNotFoundException):
        character_message = bot.storage.lexicon.get_character_message_for_command_not_found()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, LakshmiErrors.UnsupportedSitesException):
        character_message = bot.storage.lexicon.get_character_message_for_unsupported_sites()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, LakshmiErrors.NotCallOfCthulhuInvestigatorException):
        character_message = bot.storage.lexicon.get_character_message_for_not_callofcthulhu_investigator()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, LakshmiErrors.CharacterNotFoundException):
        character_message = bot.storage.lexicon.get_character_message_for_character_not_found()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, LakshmiErrors.ImageNotFoundException):
        character_message = bot.storage.lexicon.get_character_message_for_image_not_found()
        await context.send(f'{context.author.mention} {character_message}')

    elif isinstance(error, commands.CommandNotFound):
        character_message = bot.storage.lexicon.get_character_message_for_command_not_found()
        await context.send(f'{context.author.mention} {character_message}')

    else:
        original_error = getattr(error, "original", error)
        error_message = ''.join(traceback.TracebackException.from_exception(original_error).format())
        error_message = "```py\n" + error_message + "\n```"
        character_message = bot.storage.lexicon.get_character_message_to_ask_the_developer_for_help()
        message = f'{context.author.mention}\n{character_message}\n{error_message}'
        await context.send(message)

token = bot.storage.environment.get_discord_token()
bot.run(token)
