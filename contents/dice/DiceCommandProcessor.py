#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import math
import random
from decimal import Decimal

import mojimoji

class DiceCommandProcessorException(Exception):
    pass

class InvalidFormulaException(DiceCommandProcessorException):
    def __init__(self):
        super().__init__('The formula could not be interpreted. An invalid calculation formula has been specified.')

class ArgumentOutOfRangeException(DiceCommandProcessorException):
    def __init__(self):
        super().__init__('The specified number of dice exceeds the limit range.')

class InvalidCharacterException(DiceCommandProcessorException):
    def __init__(self):
        super().__init__('The dice contain invalid characters that cannot be used.')

class CommentSeparator():
    VALID_COMMENT = re.compile(r"(#|＃)")

    def __init__(self):
        self.command_line = ""
        self.comment = ""

    def separate(self, command):
        one_command_line = "".join(command.splitlines()) # 改行潰しでノーマライズ
        match = CommentSeparator.VALID_COMMENT.search(one_command_line)
        if match:
            # コメント有り
            split_command = CommentSeparator.VALID_COMMENT.split(one_command_line, maxsplit=1)
            self.command_line = mojimoji.zen_to_han(split_command[0].strip())
            self.comment = split_command[2].strip()
        else:
            # コメント無し
            self.command_line = mojimoji.zen_to_han(one_command_line.strip())
            self.comment = ""

    def is_comment(self):
        return len(self.comment) >= 1

class ComparisonSeparator():
    VALID_COMPARISON = re.compile(r"([><=]+)", re.IGNORECASE)
    VALID_CHARACTERS = re.compile(r"^([-+*/0-9\.)( ])+$", re.IGNORECASE)

    def __init__(self):
        self.dice_command = ""
        self.conditional_expression = ""
        self.comparison_name = ""
        self.comparison_value = ""

    def separate(self, command):
        # 大小判定処理
        match = ComparisonSeparator.VALID_COMPARISON.search(command)
        if match:
            # 大小記号有り
            split_command = ComparisonSeparator.VALID_COMPARISON.split(command)
            if len(split_command) != 3:
                raise InvalidFormulaException()

            self.dice_command = split_command[0].strip()
            self.conditional_expression = split_command[1].replace('=>','>=').replace('=<','<=').strip()

            comparison = split_command[2].strip()
            value_match = ComparisonSeparator.VALID_CHARACTERS.search(comparison)
            if value_match:
                self.comparison_name = ""
                self.comparison_value = comparison
            else:
                self.comparison_name = comparison
                self.comparison_value = ""
        else:
            # 大小記号無し
            self.dice_command = command

    def is_comparison(self):
        return self.conditional_expression != ""

    def get_calculation_expression(self):
        return f"{self.dice_command.lower()}{self.conditional_expression}{self.comparison_value}"

    def get_display_expression(self):
        comparison = ""
        if len(self.comparison_name) >= 1:
            comparison = f"{self.comparison_name}({self.comparison_value})"
        else:
            comparison = f"{self.comparison_value}"
        return f"{self.dice_command.lower()}{self.conditional_expression}{comparison}"


class DiceCommandProcessor():
    MAX_DICE_NUMBER = 100       # ダイスの数の最大
    MAX_DICE_SURFACE = 65536    # ダイスの面の最大

    REPLACE_DICE = re.compile(r"((\d+)d(\d+))", re.IGNORECASE)
    VALID_CHARACTERS = re.compile(r"^([-+*/a-zA-Z0-9\.)(<>= ])+$", re.IGNORECASE)
    VALID_PROCESS_CRITICAL = re.compile(r"^1d100([=><]+[-+*/0-9\.]+)?$", re.IGNORECASE)

    def __init__(self):
        self.__result = ""
        self.__calculation = ""
        self.__total = 0

        self.comment_separator: CommentSeparator = None
        self.comparison_separator: ComparisonSeparator = None
        self.judgment_result: JudgmentResult = None
        self.critical_result: CriticalResult = None

    @property
    def result(self):
        return self.__result

    @property
    def total(self):
        return self.__total

    def __replace_display_string(self, text):
        return text.replace('+','＋').replace('-','－').replace('*','×').replace('/','÷').replace('>=','≧').replace('<=','≦')

    def __replace_dice_string(self, match):
        result = ""
        number = int(match.group(2))
        if number >= DiceCommandProcessor.MAX_DICE_NUMBER:
            raise ArgumentOutOfRangeException()

        surface = int(match.group(3))
        if surface >= DiceCommandProcessor.MAX_DICE_SURFACE:
            raise ArgumentOutOfRangeException()

        result = "(" + "+".join(str(random.randint(1, surface)) for _ in range(number)) + ")"
        return result

    def execute_eval(self, formula):
        result = None
        # 安全性のチェック
        if not DiceCommandProcessor.VALID_CHARACTERS.search(formula):
            raise InvalidCharacterException()
        try:
            result = eval(formula)
        except Exception as e:
            raise InvalidFormulaException()
        return result

    def get_comment_separator(self) -> CommentSeparator:
        self.comment_separator = CommentSeparator()
        return self.comment_separator

    def get_comparison_separator(self) -> ComparisonSeparator:
        self.comparison_separator = ComparisonSeparator()
        return self.comparison_separator

    def is_judgment_result(self):
        return self.judgment_result != None

    def is_critical_result(self):
        return self.critical_result != None

    def roll(self):
        # 元コマンド逆組立て
        calculation_command_line = self.comparison_separator.get_calculation_expression()
        display_command_line = self.comparison_separator.get_display_expression()

        # ダイス本処理
        self.__calculation = DiceCommandProcessor.REPLACE_DICE.sub(self.__replace_dice_string, self.comparison_separator.dice_command)
        self.__total = math.ceil(self.execute_eval(self.__calculation)) # 小数点切り上げ

        # 大小判定
        judgment = ""
        if self.comparison_separator.is_comparison():
            self.judgment_result = JudgmentResult(self)
            judgment = self.judgment_result.result

        # クリティカル判定（D100のみ）
        critical = ""
        match = DiceCommandProcessor.VALID_PROCESS_CRITICAL.search(calculation_command_line)
        if match:
            # 1D100 only
            self.critical_result = CriticalResult(self)
            critical = self.critical_result.result

        display_one_command = self.__replace_display_string(display_command_line)
        display_calculation = self.__replace_display_string(self.__calculation)
        self.__result = f'⇒ {display_one_command} {self.comment_separator.comment}：{display_calculation} = {str(self.__total)}{judgment}{critical}'
        return self.__result


class JudgmentResult():
    def __init__(self, processor: DiceCommandProcessor):
        self.__result = ""
        self.__success = None

        # 大小判定
        judgment_string = f"{str(processor.total)}{processor.comparison_separator.conditional_expression}{processor.comparison_separator.comparison_value}"
        self.__success = bool(processor.execute_eval(judgment_string))
        if self.__success:
            self.__result = " [成功] ○"
        else:
            self.__result = " [失敗] ×"

    @property
    def result(self):
        return self.__result

    @property
    def success(self):
        return self.__success

class CriticalResult():
    def __init__(self, processor: DiceCommandProcessor):
        self.__result = ""
        self.__critical = False
        self.__fumble = False

        # 1D100 only
        if processor.total <= 5:
            self.__result = "【 Critical! 】"
            self.__critical = True
        elif processor.total >= 96:
            self.__result = "【  Fumble!  】"
            self.__fumble = True

    @property
    def result(self):
        return self.__result

    @property
    def critical(self):
        return self.__critical

    @property
    def fumble(self):
        return self.__fumble
