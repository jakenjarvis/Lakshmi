#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import math
import random

import mojimoji
from discord.ext import commands

from LakshmiErrors import ArgumentOutOfRangeException

def replace_dice_string(match):
    result = ""
    number = int(match.group(2))
    if number >= 100:  # ダイスの数の最大
        raise ArgumentOutOfRangeException()

    surface = int(match.group(3))
    if surface >= 65536: # ダイスの面の最大
        raise ArgumentOutOfRangeException()

    result = "(" + "+".join(str(random.randint(1, surface)) for _ in range(number)) + ")"
    return result

def replace_display_string(calculation):
    return calculation.replace('+','＋').replace('-','－').replace('*','×').replace('/','÷')

class DiceBot():
    REPLACE_DICE = re.compile(r"((\d+)d(\d+))", re.IGNORECASE)
    VALID_CHARACTERS = re.compile(r"^([-+*/a-zA-Z0-9\.)(<>= ])+$", re.IGNORECASE)
    VALID_COMMENT = re.compile(r"(#|＃)")
    VALID_COMPARISON = re.compile(r"([><=]+)", re.IGNORECASE)
    VALID_PROCESS_CRITICAL = re.compile(r"^1d100([=><]+[-+*/0-9\.]+)?$", re.IGNORECASE)

    def __init__(self):
        self.__processing_flag = False
        self.__reply_message = []

    @property
    def processing_flag(self):
        return self.__processing_flag

    @property
    def reply_message(self):
        return self.__reply_message

    def roll(self, command):
        command_line = ""
        comment = ""
        dice_command = ""
        conditional_expression = ""
        comparison_value = ""

        self.__reply_message = []

        commandlist = command.splitlines()
        for oneCommand in commandlist:
            # コメント判定
            match = DiceBot.VALID_COMMENT.search(oneCommand)
            if match:
                # コメント有り
                split_command = DiceBot.VALID_COMMENT.split(oneCommand, maxsplit=1)
                command_line = split_command[0].strip()
                comment = split_command[2].strip()
            else:
                # コメント無し
                command_line = oneCommand.strip()
                comment = ""

            # コマンドの整理
            fixedOneCommand = mojimoji.zen_to_han(command_line).replace(' ','')
            # 安全性のチェック
            check = DiceBot.VALID_CHARACTERS.search(fixedOneCommand)
            if check:
                # 大小判定処理
                match = DiceBot.VALID_COMPARISON.search(fixedOneCommand)
                if match:
                    # 大小記号有り
                    split_command = DiceBot.VALID_COMPARISON.split(fixedOneCommand)
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
                calculation = DiceBot.REPLACE_DICE.sub(replace_dice_string, dice_command)
                total = math.ceil(self.__execute_eval(calculation)) # 小数点切り上げ
                displayOneCommand = replace_display_string(fixedOneCommand).lower()
                displayCalculation = replace_display_string(calculation)

                # 大小判定
                judgment_result = ""
                if conditional_expression != "":
                    judgment_string = str(total) + conditional_expression + comparison_value
                    if self.__execute_eval(judgment_string):
                        judgment_result = " [成功] ○"
                    else:
                        judgment_result = " [失敗] ×"

                # クリティカル判定（D100のみ）
                critical_result = ""
                match = DiceBot.VALID_PROCESS_CRITICAL.search(fixedOneCommand)
                if match:
                    # 1D100 only
                    if total <= 5:
                        critical_result = "【 Critical! 】"
                    elif total >= 96:
                        critical_result = "【  Fumble!  】"

                self.__reply_message.append(f'⇒ {displayOneCommand} {comment}： {displayCalculation} = {str(total)}{judgment_result}{critical_result}')
                self.__processing_flag = True

    def __execute_eval(self, formula):
        result = None
        try:
            result = eval(formula)
        except Exception as e:
            raise commands.CommandNotFound()
        return result
