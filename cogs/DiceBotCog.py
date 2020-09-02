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

    @commands.command(description="(P)percent: 1d100固定のパーセント指定でダイスを振ります。")
    async def p(self, context, *, command):
        diceBot = DiceBot()
        try:
            normalize_commands = self.bot.normalize_commands(command)
            # メッセージの組み立て
            diceBot.append_reply_message(f'{context.author.mention}')
            # ダイスロール
            diceBot.percent(normalize_commands)

            # 処理後通知
            if diceBot.processing_flag:
                await context.send("\n".join(diceBot.reply_message))
            else:
                await self.bot.on_command_error(context, commands.CommandNotFound())

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @commands.command(description="(VS)versus: 対抗ロールでダイスを振ります。")
    async def vs(self, context, *, command):
        diceBot = DiceBot()
        try:
            normalize_commands = self.bot.normalize_commands(command)
            # メッセージの組み立て
            diceBot.append_reply_message(f'{context.author.mention}')
            # ダイスロール
            diceBot.versus(normalize_commands)

            # 処理後通知
            if diceBot.processing_flag:
                await context.send("\n".join(diceBot.reply_message))
            else:
                await self.bot.on_command_error(context, commands.CommandNotFound())

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @commands.command(description="(F)fate: mDn形式で面を指定してダイスを振ります。")
    async def f(self, context, *, command):
        diceBot = DiceBot()
        try:
            normalize_commands = self.bot.normalize_commands(command)
            # メッセージの組み立て
            diceBot.append_reply_message(f'{context.author.mention}')
            # ダイスロール
            diceBot.roll(normalize_commands)

            # 処理後通知
            if diceBot.processing_flag:
                await context.send("\n".join(diceBot.reply_message))
            else:
                await self.bot.on_command_error(context, commands.CommandNotFound())

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @commands.command(description="(SF)secret fate: mDn形式で面を指定してダイスを振り、DMで結果を返します。")
    async def sf(self, context, *, command):
        diceBot = DiceBot()
        try:
            normalize_commands = self.bot.normalize_commands(command)
            # メッセージの組み立て NOTE: DMするのでメンションは付けない
            #diceBot.append_reply_message(f'{context.author.mention}')
            # ダイスロール
            diceBot.roll(normalize_commands)

            # 処理後通知
            if diceBot.processing_flag:
                await context.author.send("\n".join(diceBot.reply_message))
            else:
                await self.bot.on_command_error(context, commands.CommandNotFound())

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

def setup(bot):
    bot.add_cog(DiceBotCog(bot))
