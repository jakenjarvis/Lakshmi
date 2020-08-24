#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import math
import random

import mojimoji
from discord.ext import commands

from DiceBot import DiceBot

class DiceBotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.command()
    async def hello(self, context):
        await context.send('やっほー')

    @commands.command()
    async def f(self, context, *, command):
        diceBot = DiceBot()
        try:
            normalize_commands = self.__normalize_commands(command)
            # ダイスロール
            diceBot.roll(normalize_commands)

            # メッセージの組み立て
            reply_message = []
            reply_message.append(f'{context.author.mention}')
            for message in diceBot.reply_message:
                reply_message.append(message)

            # 処理後通知
            if diceBot.processing_flag:
                await context.send("\n".join(reply_message))
            else:
                await self.bot.on_command_error(context, commands.CommandNotFound())

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @commands.command()
    async def sf(self, context, *, command):
        diceBot = DiceBot()
        try:
            normalize_commands = self.__normalize_commands(command)
            # ダイスロール
            diceBot.roll(normalize_commands)

            # メッセージの組み立て
            reply_message = []
            for message in diceBot.reply_message:
                reply_message.append(message)

            # 処理後通知
            if diceBot.processing_flag:
                await context.author.send("\n".join(reply_message))
            else:
                await self.bot.on_command_error(context, commands.CommandNotFound())

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    def __normalize_commands(self, command):
        # コメントがあるのでここでは.lower()しないこと。
        result = ""
        linking_command = "🎲".join(command.splitlines())
        convert_zenkaku = self.bot.regex_command.sub("🎲", linking_command).replace('　',' ')
        split_command = re.split('🎲', convert_zenkaku, flags=re.IGNORECASE)
        removal_blank_line = [row.strip() for row in split_command if row.strip() != ""]
        result = "\n".join(removal_blank_line)
        print("-----normalize_commands:\n" + result)
        return result

def setup(bot):
    bot.add_cog(DiceBotCog(bot))
