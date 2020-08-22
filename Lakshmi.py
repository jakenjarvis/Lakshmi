#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import traceback

import discord
from discord.ext import commands

from LakshmiStorage import LakshmiStorage
from LakshmiErrors import PermissionNotFound

bot = commands.Bot(command_prefix='/')
bot.storage = LakshmiStorage()


extensions = [
    'cogs.DiceBotCog',
]
for extension in extensions:
    bot.load_extension(extension)


@bot.event
async def on_command_error(context, error):
    # Throwしたいときは、以下のようにon_command_errorを呼び出す。
    # await self.bot.on_command_error(context, PermissionNotFound())

    if isinstance(error, commands.CommandNotFound):
        await context.send('ごめんなさい。何のことかよくわからなかったわ。')

    elif isinstance(error, PermissionNotFound):
        await context.send('あなたにはコマンドを実行する権限が無いようよ。')

    else:
        original_error = getattr(error, "original", error)
        error_message = ''.join(traceback.TracebackException.from_exception(original_error).format())
        error_message = "```py\n" + error_message + "\n```"
        await context.send(error_message)


token = ""
try:
    # Heroku環境
    token = os.environ['DISCORD_TOKEN']
except Exception as e:
    # ローカル環境
    with open(r"token.txt", "r", encoding="utf-8") as file:
        token = file.read()

bot.run(token)
