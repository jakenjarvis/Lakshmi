#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import math
import random
import collections
from decimal import Decimal
from typing import List, Dict, Tuple, Pattern, Match, Type

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
        self.expression_formula: str = ""
        self.comment: str = ""

    def separate(self, command: str):
        expression_formula = "".join(command.splitlines()) # 改行潰しでノーマライズ
        match = CommentSeparator.VALID_COMMENT.search(expression_formula)
        if match:
            # コメント有り
            split_command = CommentSeparator.VALID_COMMENT.split(expression_formula, maxsplit=1)
            self.expression_formula = mojimoji.zen_to_han(split_command[0].strip(), kana=False)
            self.comment = split_command[2].strip()
        else:
            # コメント無し
            self.expression_formula = mojimoji.zen_to_han(expression_formula.strip(), kana=False)
            self.comment = ""
        return self

    def is_comment(self) -> bool:
        return len(self.comment) >= 1

    def set_comment(self, comment: str):
        self.comment = str(comment)

class EvaluationExpressionSeparator():
    VALID_COMPARISON = re.compile(r"([><=]+)", re.IGNORECASE)

    def __init__(self):
        self.display_expression_formula: str = ""

        self.left_formula: str = ""
        self.calculation_comparison_operator: str = ""
        self.display_comparison_operator: str = ""
        self.right_formula: str = ""

    def separate(self, expression_formula: str):
        self.display_expression_formula = expression_formula
        # 大小判定処理
        match = EvaluationExpressionSeparator.VALID_COMPARISON.search(expression_formula)
        if match:
            # 大小記号有り
            split_command = EvaluationExpressionSeparator.VALID_COMPARISON.split(expression_formula)
            if len(split_command) != 3:
                raise InvalidFormulaException()

            self.left_formula = split_command[0].strip()
            self.calculation_comparison_operator = split_command[1].replace('=>','>=').replace('=<','<=').strip()
            self.display_comparison_operator = split_command[1].replace('=>','>=').replace('=<','<=').strip()
            self.right_formula = split_command[2].strip()
        else:
            # 大小記号無し
            self.left_formula = expression_formula.strip()
        return self

    def is_comparison_operator(self) -> bool:
        return self.calculation_comparison_operator != ""

class FormulaSeparator():
    VALID_BRACKETS_CHARACTERS = re.compile(r"([)(-+*/])", re.IGNORECASE)
    VALID_FORMULA_CHARACTERS = re.compile(r"(\d+d\d+|[-+*/0-9\.]+)", re.IGNORECASE)
    VALID_DICE_CHARACTERS = re.compile(r"^((\d+)d(\d+))$", re.IGNORECASE)

    def __init__(self):
        self.calculation_formula_left = ""
        self.calculation_formula_center = ""
        self.calculation_formula_right = ""
        self.display_formula_left = ""
        self.display_formula_center = ""
        self.display_formula_right = ""

        self.__need_name_replacement: bool = False
        self.__need_dice_replacement: bool = False

        self.__brackets: List[str] = []
        self.__evaluations: List[str] = []
        self.__counter: collections.Counter = None

    def separate(self, formula: str):
        #print(f"----formula: {formula}")
        # 記号区切り
        split_brackets = FormulaSeparator.VALID_BRACKETS_CHARACTERS.split(formula.replace(' ',''))
        self.__brackets = [item for item in split_brackets if item.strip() != ""]
        #print(self.__brackets)

        # 分割文字の評価
        self.__evaluations = self.__evaluation(self.__brackets)
        self.__counter = collections.Counter(self.__evaluations)

        # 名前置換の必要性
        if self.__counter["C"] >= 1:
            self.__need_name_replacement = True
        if self.__counter["D"] >= 1:
            self.__need_dice_replacement = True

        # 吸着（１～３つの塊に分ける）
        # Cが２個以上ある場合は、泥臭く組み立てる必要あり。
        # Cに挟まれているものはすべて１つのCとみなす。
        # Cに挟まれているLRは、直近の対応するLRまで吸着する。
        stock_left = []
        stock_center = []
        stock_right = []
        count_center = 0
        adsorption_count_cl = 0
        adsorption_count_cr = 0
        for index, item in enumerate(self.__brackets):
            if self.__evaluations[index] == "C":
                # Cの時
                count_center += 1
                stock_center.append(item)
            else:
                # C以外の時
                if count_center == 0:
                    # Cにぶち当たる前
                    stock_left.append(item)
                elif count_center <= self.__counter["C"] - 1:
                    # Cにぶち当たり、まだCがある中間
                    stock_center.append(item)
                    # Cに挟まれたLRをカウント
                    if self.__evaluations[index] == "L":
                        adsorption_count_cl += 1
                        adsorption_count_cr -= 1
                    elif self.__evaluations[index] == "R":
                        adsorption_count_cl -= 1
                        adsorption_count_cr += 1

                    if (adsorption_count_cr >= 1):
                        # Cに挟まれたRの数だけLを吸着
                        for rev_index in reversed(range(0, len(stock_left))):
                            stock_center.insert(0, stock_left.pop())
                            if self.__evaluations[rev_index] == "L":
                                break
                        adsorption_count_cr -= 1
                else:
                    # 最後のCにぶち当たった後
                    if (adsorption_count_cl >= 1):
                        stock_center.append(item)
                        if self.__evaluations[index] == "R":
                            # Cに挟まれたLの数だけRを吸着
                            adsorption_count_cl -= 1
                    else:
                        stock_right.append(item)

        # 最後の組み立て
        self.calculation_formula_left = "".join(stock_left)
        self.calculation_formula_center = "".join(stock_center)
        self.calculation_formula_right = "".join(stock_right)
        self.display_formula_left = "".join(stock_left)
        self.display_formula_center = "".join(stock_center)
        self.display_formula_right = "".join(stock_right)
        #print(f"calculation_formula_left   : {self.calculation_formula_left}")
        #print(f"calculation_formula_center : {self.calculation_formula_center}")
        #print(f"calculation_formula_right  : {self.calculation_formula_right}")
        return self

    def __evaluation(self, brackets):
        result: List[str] = []
        for item in brackets:
            if item == "(":
                # 括弧左
                result.append("L")
            elif item == ")":
                # 括弧右
                result.append("R")
            elif FormulaSeparator.VALID_DICE_CHARACTERS.search(item):
                # 計算可能文字（ダイスnDm文字）
                result.append("D")
            elif FormulaSeparator.VALID_FORMULA_CHARACTERS.search(item):
                # 計算可能文字（その他）
                result.append("F")
            else:
                # その他の文字（名前付き置換対象）
                result.append("C")
        #print(result)
        return result

    def is_need_name_replacement(self) -> bool:
        return self.__need_name_replacement

    def is_need_dice_replacement(self) -> bool:
        return self.__need_dice_replacement

    def get_calculation_formula(self) -> str:
        return f"{self.calculation_formula_left}{self.calculation_formula_center}{self.calculation_formula_right}"

    def get_display_formula(self) -> str:
        return f"{self.display_formula_left}{self.display_formula_center}{self.display_formula_right}"

class ReplacerBase():
    def __init__(self, **kwargs):
        pass

    def replace_comparison_operator(self, separator: EvaluationExpressionSeparator):
        raise NotImplementedError()

    def replace_formula(self, separator: FormulaSeparator):
        raise NotImplementedError()

class DiceReplacer(ReplacerBase):
    MAX_DICE_NUMBER = 100       # ダイスの数の最大
    MAX_DICE_SURFACE = 65536    # ダイスの面の最大
    REPLACE_DICE = re.compile(r"((\d+)d(\d+))", re.IGNORECASE)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dice_stock: List[Tuple[str,str]] = []
        self.dice_stock_index = 0

    def __replace_calculation_dice_string(self, match: Match) -> str:
        result = ""
        number = int(match.group(2))
        if number >= DiceReplacer.MAX_DICE_NUMBER:
            raise ArgumentOutOfRangeException()

        surface = int(match.group(3))
        if surface >= DiceReplacer.MAX_DICE_SURFACE:
            raise ArgumentOutOfRangeException()

        dice_command = f"{number}d{surface}"
        dice_result = "+".join(str(random.randint(1, surface)) for _ in range(number))
        self.dice_stock.append((dice_command, dice_result))
        result = f"({dice_result})"
        return result

    def __replace_display_dice_string(self, match: Match) -> str:
        # NOTE: ここではダイスを振らずに、計算用で出した結果を使う。（結果が異なってしまう）
        result = ""
        dice_command = self.dice_stock[self.dice_stock_index][0]
        dice_result = self.dice_stock[self.dice_stock_index][1]
        #result = f"({dice_command}:{dice_result})"
        result = f"({dice_result})"
        self.dice_stock_index += 1
        return result

    # overwride
    def replace_comparison_operator(self, separator: EvaluationExpressionSeparator):
        return self

    # overwride
    def replace_formula(self, separator: FormulaSeparator):
        separator.calculation_formula_left = DiceReplacer.REPLACE_DICE.sub(self.__replace_calculation_dice_string, separator.calculation_formula_left)
        separator.calculation_formula_center = separator.calculation_formula_center
        separator.calculation_formula_right = DiceReplacer.REPLACE_DICE.sub(self.__replace_calculation_dice_string, separator.calculation_formula_right)
        separator.display_formula_left = DiceReplacer.REPLACE_DICE.sub(self.__replace_display_dice_string, separator.display_formula_left)
        separator.display_formula_center = separator.display_formula_center
        separator.display_formula_right = DiceReplacer.REPLACE_DICE.sub(self.__replace_display_dice_string, separator.display_formula_right)
        return self

class OperatorSymbolReplacer(ReplacerBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __replace_display_string(self, text: str) -> str:
        return text.replace('+','＋').replace('-','－').replace('*','×').replace('/','÷') \
            .replace('>=','≧').replace('<=','≦').replace('>','＞').replace('<','＜')

    # overwride
    def replace_comparison_operator(self, separator: EvaluationExpressionSeparator):
        separator.display_expression_formula = self.__replace_display_string(separator.display_expression_formula)

        separator.calculation_comparison_operator = separator.calculation_comparison_operator
        separator.display_comparison_operator = self.__replace_display_string(separator.display_comparison_operator)
        return self

    # overwride
    def replace_formula(self, separator: FormulaSeparator):
        #TODO: 全角の四則演算記号を半角に変換する処理をcalculation側に入れる。
        separator.calculation_formula_left = separator.calculation_formula_left
        separator.calculation_formula_center = separator.calculation_formula_center
        separator.calculation_formula_right = separator.calculation_formula_right
        separator.display_formula_left = self.__replace_display_string(separator.display_formula_left)
        separator.display_formula_center = separator.display_formula_center
        separator.display_formula_right = self.__replace_display_string(separator.display_formula_right)
        return self

class CalculatorBase():
    VALID_CHARACTERS = re.compile(r"^([-+*/0-9\.)(<>= ])+$", re.IGNORECASE)
    def __init__(self):
        pass

    def execute_eval(self, formula: str) -> any:
        result = None
        # 安全性のチェック
        if not CalculatorBase.VALID_CHARACTERS.search(formula):
            raise InvalidCharacterException()
        try:
            result = eval(formula)
        except Exception as e:
            raise InvalidFormulaException()
        return result

class FormulaCalculator(CalculatorBase):
    def __init__(self):
        super().__init__()
        self.total: int = 0

    def calculate_formula(self, formula: str) -> int:
        self.total = math.ceil(self.execute_eval(formula)) # 小数点切り上げ
        return self

class EvaluationExpressionCalculator(CalculatorBase):
    def __init__(self):
        super().__init__()
        self.success: bool = None

    def calculate_evaluation_expression(self, evaluation_expression: str) -> bool:
        self.success = bool(self.execute_eval(evaluation_expression))
        return self

class DiceCommandProcessor():
    def __init__(self):
        self.__result: str = ""

        self.comment_separator: CommentSeparator = CommentSeparator()
        self.evaluation_expression_separator: EvaluationExpressionSeparator = EvaluationExpressionSeparator()
        self.left_formula_separator: FormulaSeparator = FormulaSeparator()
        self.right_formula_separator: FormulaSeparator = FormulaSeparator()
        self.left_formula_calculator: FormulaCalculator = FormulaCalculator()
        self.right_formula_calculator: FormulaCalculator = FormulaCalculator()
        self.evaluation_expression_calculator: EvaluationExpressionCalculator = EvaluationExpressionCalculator()

        self.replacer_types: List[Tuple[Type[ReplacerBase], Dict[str,any]]] = [] # インスタンスを保持しない。タイプとパラメータ
        self.replacers: List[ReplacerBase] = [] # 生成したインスタンスの格納

        self.append_replacer_types(DiceReplacer)
        self.append_replacer_types(OperatorSymbolReplacer)

    def append_replacer_types(self, type_replacer: type, **kwargs):
        self.replacer_types.append((type_replacer, kwargs))

    def create_replacer(self, type_replacer: type, **kwargs) -> ReplacerBase:
        #print(f"create_replacer: {type_replacer} (kwargs: {kwargs})")
        result = type_replacer(**kwargs)
        self.replacers.append(result)
        return result

    def find_replacers(self, type_replacer: type) -> List[ReplacerBase]:
        return [replacer for replacer in self.replacers if type(replacer) is type_replacer]

    @property
    def result(self) -> str:
        return self.__result

    def get_comment_separator(self) -> CommentSeparator:
        return self.comment_separator

    def get_evaluation_expression_separator(self) -> EvaluationExpressionSeparator:
        return self.evaluation_expression_separator

    def get_left_formula_separator(self) -> FormulaSeparator:
        return self.left_formula_separator

    def get_right_formula_separator(self) -> FormulaSeparator:
        return self.right_formula_separator

    def get_left_formula_calculator(self) -> FormulaCalculator:
        return self.left_formula_calculator

    def get_right_formula_calculator(self) -> FormulaCalculator:
        return self.right_formula_calculator

    def get_evaluation_expression_calculator(self) -> EvaluationExpressionCalculator:
        return self.evaluation_expression_calculator

    def execute_evaluation_expression(self):
        self.evaluation_expression_separator.separate(self.comment_separator.expression_formula)

        if self.evaluation_expression_separator.is_comparison_operator():
            # Left and Right
            self.left_formula_separator.separate(self.evaluation_expression_separator.left_formula)
            self.right_formula_separator.separate(self.evaluation_expression_separator.right_formula)
        else:
            # Left only
            self.left_formula_separator.separate(self.evaluation_expression_separator.left_formula)
        return self

    def execute_replacers(self):
        self.replacers = []
        if self.evaluation_expression_separator.is_comparison_operator():
            # Left and Right
            for replacer, kwargs in self.replacer_types:
                # 新しいインスタンスを生成して実行
                temp_replacer = self.create_replacer(replacer, **kwargs)
                temp_replacer.replace_formula(self.left_formula_separator)

                temp_replacer = self.create_replacer(replacer, **kwargs)
                temp_replacer.replace_formula(self.right_formula_separator)

            for replacer, kwargs in self.replacer_types:
                # 新しいインスタンスを生成して実行
                temp_replacer = self.create_replacer(replacer, **kwargs)
                temp_replacer.replace_comparison_operator(self.evaluation_expression_separator)
        else:
            # Left only
            for replacer, kwargs in self.replacer_types:
                # 新しいインスタンスを生成して実行
                temp_replacer = self.create_replacer(replacer, **kwargs)
                temp_replacer.replace_formula(self.left_formula_separator)
        return self

    def execute_calculate(self):
        if self.evaluation_expression_separator.is_comparison_operator():
            # Left and Right
            # 左右の計算
            self.left_formula_calculator.calculate_formula(self.left_formula_separator.get_calculation_formula())
            self.right_formula_calculator.calculate_formula(self.right_formula_separator.get_calculation_formula())

            # 評価計算
            left_total = self.left_formula_calculator.total
            right_total = self.right_formula_calculator.total
            comparison_operator = self.evaluation_expression_separator.calculation_comparison_operator

            expression = f"{left_total}{comparison_operator}{right_total}"
            self.evaluation_expression_calculator.calculate_evaluation_expression(expression)
        else:
            # Left only
            # 左の計算
            self.left_formula_calculator.calculate_formula(self.left_formula_separator.get_calculation_formula())
        return self

    def generate_dice_result_string(self) -> str:
        self.__result = ""

        judgment: str = ""
        critical: str = ""
        mark: str = ""
        left_display_formula: str = ""
        right_display_formula: str = ""
        left_total: int = 0
        right_total: int = 0
        left_total_string: str = ""
        right_total_string: str = ""

        if self.evaluation_expression_separator.is_comparison_operator():
            # Left and Right
            left_total = self.left_formula_calculator.total
            right_total = self.right_formula_calculator.total

            # 大小判定
            if self.evaluation_expression_calculator.success:
                judgment = " [成功] "
                mark = "⭕"
            else:
                judgment = " [失敗] "
                mark = "❌"

            left_total_string = f"{left_total}"
            right_total_string = f"{right_total}"
        else:
            # Left only
            left_total = self.left_formula_calculator.total

            left_total_string = f"{left_total}"
            right_total_string = f""

        # 使用ダイスリストの作成
        all_dice_stock: List[Tuple[str,str]] = []
        for temp_replacer in self.replacers:
            if type(temp_replacer) is DiceReplacer:
                all_dice_stock.extend(temp_replacer.dice_stock)
        #print(all_dice_stock)

        # クリティカル判定（D100のみ）
        if len(all_dice_stock) == 1:
            dice_command = all_dice_stock[0][0]
            dice_result = all_dice_stock[0][1]
            # 1D100 only
            if dice_command == "1d100":
                if int(dice_result) <= 5:
                    critical = "【 Critical! 】"
                elif int(dice_result) >= 96:
                    critical = "【  Fumble!  】"

        left_display_formula = self.left_formula_separator.get_display_formula()
        right_display_formula = self.right_formula_separator.get_display_formula()
        display_comparison_operator = self.evaluation_expression_separator.display_comparison_operator
        display_expression = f"{left_display_formula}{display_comparison_operator}{right_display_formula}"

        display_expression_formula = self.evaluation_expression_separator.display_expression_formula

        total_string = f"{left_total_string}{display_comparison_operator}{right_total_string}"
        comment = f"#{self.comment_separator.comment}" if len(self.comment_separator.comment) >= 1 else ""

        self.__result = f'⇒ {mark} {display_expression_formula} = {display_expression} → {total_string} {comment}{judgment}{critical}'
        return self.__result

    def roll(self, command: str) -> str:
        self.comment_separator.separate(command)
        self.execute_evaluation_expression()
        self.execute_replacers()
        self.execute_calculate()
        return self.generate_dice_result_string()
