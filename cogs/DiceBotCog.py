#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import random

import mojimoji
from discord.ext import commands

from LakshmiErrors import PermissionNotFound

def replace_dice_string(match):
    result = ""
    number = int(match.group(2))
    surface = int(match.group(3))
    result = "(" + "+".join(str(random.randint(1, surface)) for _ in range(number)) + ")"
    return result

def replace_display_string(calculation):
    result = calculation
    result = result.replace('+','＋')
    result = result.replace('-','－')
    result = result.replace('*','×')
    result = result.replace('/','÷')
    return result

class DiceBotCog(commands.Cog):
    VALID_CHARACTERS = re.compile(r"^([-+*/a-zA-Z0-9)(<>= ])+$", re.IGNORECASE)
    VALID_DICE = re.compile(r"((\d+)d(\d+))", re.IGNORECASE)

    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.command()
    async def hello(self, context):
        await context.send('やっほー')

    @commands.command()
    async def cf(self, context, *, command):
        print(command)
        processingFlag = False
        try:
            # TODO: コマンドの連結と再分割処理
            # TODO: ＃コメント処理
            # TODO: ２行目以降の処理がおかしい/cfが入ってる、消す処理追加
            # TODO: 返却文字数のチェック
            # TODO: トータルの小数点端数切り上げ
            commandlist = command.splitlines()
            for oneCommand in commandlist:
                fixedOneCommand = mojimoji.zen_to_han(str(oneCommand)).replace(' ','')
                # 安全性のチェック
                check = DiceBotCog.VALID_CHARACTERS.search(str(fixedOneCommand))
                if check:
                    calculation = DiceBotCog.VALID_DICE.sub(replace_dice_string, str(fixedOneCommand))
                    total = eval(calculation)
                    displayOneCommand = replace_display_string(fixedOneCommand).lower()
                    displayCalculation = replace_display_string(calculation)
                    await context.send(f'{context.author.mention} {displayOneCommand} = {displayCalculation} = {str(total)}')
                    processingFlag = True

            if not processingFlag:
                await self.bot.on_command_error(context, commands.CommandNotFound())

        except Exception as e:
            await self.bot.on_command_error(context, commands.CommandNotFound())

def setup(bot):
    bot.add_cog(DiceBotCog(bot))
