#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import math
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
    return calculation.replace('+','＋').replace('-','－').replace('*','×').replace('/','÷')

class DiceBotCog(commands.Cog):
    DICE_ROLL_COMMAND = ":f"
    REPLACE_COMMAND = re.compile(r"(([:：])([fFｆＦ]))")
    REPLACE_DICE = re.compile(r"((\d+)d(\d+))", re.IGNORECASE)
    VALID_CHARACTERS = re.compile(r"^([-+*/a-zA-Z0-9\.)(<>= ])+$", re.IGNORECASE)
    VALID_COMMENT = re.compile(r"(#|＃)")
    VALID_COMPARISON = re.compile(r"([><=]+)", re.IGNORECASE)
    VALID_PROCESS_CRITICAL = re.compile(r"^1d100([=><]+[-+*/0-9\.]+)?$", re.IGNORECASE)

    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.command()
    async def hello(self, context):
        await context.send('やっほー')

    @commands.command()
    async def f(self, context, *, command):
        print(command)
        processingFlag = False
        try:
            # TODO: 返却文字数のチェック
            command_line = ""
            comment = ""
            dice_command = ""
            conditional_expression = ""
            comparison_value = ""

            reply_message = []
            reply_message.append(f'{context.author.mention}')
            normalize_commands = self.normalize_commands(command)
            commandlist = normalize_commands.splitlines()
            for oneCommand in commandlist:
                # コメント判定
                match = DiceBotCog.VALID_COMMENT.search(oneCommand)
                if match:
                    # コメント有り
                    split_command = DiceBotCog.VALID_COMMENT.split(oneCommand, maxsplit=1)
                    command_line = split_command[0].strip()
                    comment = split_command[2].strip()
                else:
                    # コメント無し
                    command_line = oneCommand.strip()
                    comment = ""

                # コマンドの整理
                fixedOneCommand = mojimoji.zen_to_han(command_line).replace(' ','')
                # 安全性のチェック
                check = DiceBotCog.VALID_CHARACTERS.search(fixedOneCommand)
                if check:
                    # 大小判定処理
                    match = DiceBotCog.VALID_COMPARISON.search(fixedOneCommand)
                    if match:
                        # 大小記号有り
                        split_command = DiceBotCog.VALID_COMPARISON.split(fixedOneCommand)
                        if len(split_command) == 3:
                            dice_command = split_command[0].strip()
                            conditional_expression = split_command[1].replace('=>','>=').replace('=<','<=').strip()
                            comparison_value = split_command[2].strip()
                        else:
                            raise commands.CommandNotFound()
                    else:
                        # 大小記号無し
                        dice_command = fixedOneCommand

                    # ダイス本処理
                    calculation = DiceBotCog.REPLACE_DICE.sub(replace_dice_string, dice_command)
                    total = math.ceil(eval(calculation)) # 小数点切り上げ
                    displayOneCommand = replace_display_string(fixedOneCommand).lower()
                    displayCalculation = replace_display_string(calculation)

                    # 大小判定
                    judgment_result = ""
                    if conditional_expression != "":
                        judgment_string = str(total) + conditional_expression + comparison_value
                        if eval(judgment_string):
                            judgment_result = " | Success!"
                        else:
                            judgment_result = " | Failure!"

                    # クリティカル判定（D100のみ）
                    critical_result = ""
                    match = DiceBotCog.VALID_PROCESS_CRITICAL.search(fixedOneCommand)
                    if match:
                        # 1D100 only
                        if total <= 5:
                            critical_result = " 【 Critical! 】"
                        elif total >= 96:
                            critical_result = " 【  Fumble!  】"

                    reply_message.append(f'{displayOneCommand} {comment} = {displayCalculation} = {str(total)}{judgment_result}{critical_result}')
                    processingFlag = True

            if processingFlag:
                await context.send("\n".join(reply_message))
            else:
                await self.bot.on_command_error(context, commands.CommandNotFound())

        except Exception as e:
            await self.bot.on_command_error(context, commands.CommandNotFound())

    def normalize_commands(self, command):
        result = ""
        # コメントがあるのでここでは.lower()しない。
        linking_command = "🎲".join(command.splitlines())
        convert_zenkaku = DiceBotCog.REPLACE_COMMAND.sub(DiceBotCog.DICE_ROLL_COMMAND, linking_command).replace('　',' ')
        split_command = re.split(f'{DiceBotCog.DICE_ROLL_COMMAND}|🎲', convert_zenkaku, flags=re.IGNORECASE)
        removal_blank_line = [row.strip() for row in split_command if row.strip() != ""]
        result = "\n".join(removal_blank_line)
        print(result)
        return result

def setup(bot):
    bot.add_cog(DiceBotCog(bot))
