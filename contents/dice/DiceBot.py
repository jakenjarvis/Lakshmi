#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import math
import random

import mojimoji
from discord.ext import commands

import LakshmiErrors

def replace_dice_string(match):
    result = ""
    number = int(match.group(2))
    if number >= 100:  # ダイスの数の最大
        raise LakshmiErrors.ArgumentOutOfRangeException()

    surface = int(match.group(3))
    if surface >= 65536: # ダイスの面の最大
        raise LakshmiErrors.ArgumentOutOfRangeException()

    result = "(" + "+".join(str(random.randint(1, surface)) for _ in range(number)) + ")"
    return result

def replace_display_string(calculation):
    return calculation.replace('+','＋').replace('-','－').replace('*','×').replace('/','÷')

class LineCommentSeparator():
    VALID_COMMENT = re.compile(r"(#|＃)")

    def __init__(self, one_command_line):
        self.__command_line = ""
        self.__comment = ""

        match = LineCommentSeparator.VALID_COMMENT.search(one_command_line)
        if match:
            # コメント有り
            split_command = LineCommentSeparator.VALID_COMMENT.split(one_command_line, maxsplit=1)
            self.__command_line = split_command[0].strip()
            self.__comment = split_command[2].strip()
        else:
            # コメント無し
            self.__command_line = one_command_line.strip()
            self.__comment = ""

    @property
    def command_line(self):
        return self.__command_line

    @property
    def comment(self):
        return self.__comment

    def is_comment(self):
        return len(self.__comment) >= 1

class DiceBot():
    REPLACE_DICE = re.compile(r"((\d+)d(\d+))", re.IGNORECASE)
    VALID_CHARACTERS = re.compile(r"^([-+*/a-zA-Z0-9\.)(<>= ])+$", re.IGNORECASE)
    VALID_COMPARISON = re.compile(r"([><=]+)", re.IGNORECASE)
    VALID_PROCESS_CRITICAL = re.compile(r"^1d100([=><]+[-+*/0-9\.]+)?$", re.IGNORECASE)

    def __init__(self):
        self.__processing_flag = False
        self.__reply_message = []
        self.__critical = False
        self.__fumble = False

    @property
    def processing_flag(self):
        return self.__processing_flag

    @property
    def reply_message(self):
        return self.__reply_message

    @property
    def critical(self):
        return self.__critical

    @property
    def fumble(self):
        return self.__fumble

    def append_reply_message(self, message):
        self.__reply_message.append(message)

    def percent(self, command):
        commandlist = command.splitlines()
        for oneCommand in commandlist:
            # コメント判定
            commandComment = ""
            lc_separator = LineCommentSeparator(oneCommand)
            if lc_separator.is_comment():
                # コメント有り
                commandComment = f' #{lc_separator.comment}'
            else:
                # コメント無し
                commandComment = ""

            # コマンドの整理
            fixedOneCommand = mojimoji.zen_to_han(lc_separator.command_line).replace(' ','')
            # 安全性のチェック
            check = DiceBot.VALID_CHARACTERS.search(fixedOneCommand)
            if check:
                command_line = fixedOneCommand.split(" ")
                removal_blank = [word.strip() for word in command_line if word.strip() != ""]
                print(removal_blank)

                if not len(removal_blank) >= 1:
                    raise commands.CommandNotFound()
                percent = int(removal_blank[0])

                self.roll(f'1d100<={str(percent)}{commandComment}')

    def versus(self, command):
        # :vs 能動側(する側) 受動側(される側)
        # (能動側ー受動側)×5＝差分を行い、50＋差分＝成功値で決定。それを1d100で振って成否の判断を行う。
        # 例)DEX対抗の場合
        #  能動側の数値:9、受動側の数値:10
        #  (9-10)×5=-5、50+(-5)=45% ⇒ 1d100<=45 #対抗の成功判定
        commandlist = command.splitlines()
        for oneCommand in commandlist:
            # コメント判定
            commandComment = ""
            lc_separator = LineCommentSeparator(oneCommand)
            if lc_separator.is_comment():
                # コメント有り
                if "対抗" in lc_separator.comment:
                    commandComment = f' #{lc_separator.comment}'
                else:
                    commandComment = f' #対抗{lc_separator.comment}'
            else:
                # コメント無し
                commandComment = " #対抗ロール"

            # コマンドの整理
            fixedOneCommand = mojimoji.zen_to_han(lc_separator.command_line)
            # 安全性のチェック
            check = DiceBot.VALID_CHARACTERS.search(fixedOneCommand)
            if check:
                command_line = fixedOneCommand.split(" ")
                removal_blank = [word.strip() for word in command_line if word.strip() != ""]
                print("removal_blank: " + str(removal_blank))

                if not len(removal_blank) >= 2:
                    raise commands.CommandNotFound()

                active_side = int(removal_blank[0])
                passive_side = int(removal_blank[1])
                percent = 50 + ((active_side - passive_side) * 5)

                self.roll(f'1d100<={str(percent)}{commandComment}')

    def roll(self, command):
        dice_command = ""
        conditional_expression = ""
        comparison_value = ""

        commandlist = command.splitlines()
        for oneCommand in commandlist:
            # コメント判定
            lc_separator = LineCommentSeparator(oneCommand)
            # コマンドの整理
            fixedOneCommand = mojimoji.zen_to_han(lc_separator.command_line).replace(' ','')
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
                        self.__critical = True
                    elif total >= 96:
                        critical_result = "【  Fumble!  】"
                        self.__fumble = True

                self.__reply_message.append(f'⇒ {displayOneCommand} {lc_separator.comment}： {displayCalculation} = {str(total)}{judgment_result}{critical_result}')
                self.__processing_flag = True

    def __execute_eval(self, formula):
        result = None
        try:
            result = eval(formula)
        except Exception as e:
            raise commands.CommandNotFound()
        return result
