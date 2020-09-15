#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from contents.dice.DiceCommandProcessor import DiceCommandProcessor, InvalidFormulaException, CalculatorBase

class CallOfCthulhuDice(DiceCommandProcessor):
    def __init__(self):
        super().__init__()

    def percent(self, command):
        self.comment_separator.separate(command)

        value = self.comment_separator.expression_formula
        new_command = f"1d100<={value}"
        self.comment_separator.expression_formula = new_command

        self.execute_evaluation_expression()
        self.execute_replacers()
        self.execute_calculate()
        return self.generate_dice_result_string()

    def versus(self, command):
        # :vs 能動側(する側) 受動側(される側)
        # (能動側ー受動側)×5＝差分を行い、50＋差分＝成功値で決定。それを1d100で振って成否の判断を行う。
        # 例)DEX対抗の場合
        #  能動側の数値:9、受動側の数値:10
        #  (9-10)×5=-5、50+(-5)=45% ⇒ 1d100<=45 #対抗の成功判定
        self.comment_separator.separate(command)

        command_string = self.comment_separator.expression_formula

        command_line = command_string.split(" ")
        removal_blank = [word.strip() for word in command_line if word.strip() != ""]
        #print("removal_blank: " + str(removal_blank))
        if not len(removal_blank) >= 2:
            raise InvalidFormulaException()

        calculator = CalculatorBase()
        active_side = int(calculator.execute_eval(removal_blank[0]))
        passive_side = int(calculator.execute_eval(removal_blank[1]))

        name = f"{active_side}vs{passive_side}"
        value = 50 + ((active_side - passive_side) * 5)

        new_command = f"1d100<={value}"
        self.comment_separator.expression_formula = new_command

        if self.comment_separator.is_comment():
            # コメント有り
            if "対抗" in self.comment_separator.comment:
                new_comment = f'{name} {self.comment_separator.comment}'
            else:
                new_comment = f'{name} 対抗{self.comment_separator.comment}'
        else:
            # コメント無し
            new_comment = f"{name} 対抗ロール"
        self.comment_separator.set_comment(new_comment)

        self.execute_evaluation_expression()
        self.execute_replacers()
        self.execute_calculate()
        return self.generate_dice_result_string()
