#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from contents.dice.DiceCommandProcessor import DiceCommandProcessor, InvalidFormulaException

class CallOfCthulhuDice(DiceCommandProcessor):
    def __init__(self):
        super().__init__()

    def percent(self, command):
        comment_separator = self.get_comment_separator().separate(command)
        #print(comment_separator.command_line)
        #print(comment_separator.comment)

        comparison_separator = self.get_comparison_separator().separate(comment_separator.command_line)
        #print(comparison_separator.comparison_name)
        #print(comparison_separator.comparison_value)

        command_string = comparison_separator.dice_command

        name = command_string
        value = int(self.execute_eval(command_string))

        comparison_separator.set_dice_command("1d100")
        comparison_separator.set_conditional_expression("<=")
        comparison_separator.set_comparison_name(name)
        comparison_separator.set_comparison_value(value)

        return self.dice_command_roll()

    def versus(self, command):
        # :vs 能動側(する側) 受動側(される側)
        # (能動側ー受動側)×5＝差分を行い、50＋差分＝成功値で決定。それを1d100で振って成否の判断を行う。
        # 例)DEX対抗の場合
        #  能動側の数値:9、受動側の数値:10
        #  (9-10)×5=-5、50+(-5)=45% ⇒ 1d100<=45 #対抗の成功判定
        comment_separator = self.get_comment_separator().separate(command)
        #print(comment_separator.command_line)
        #print(comment_separator.comment)
        if comment_separator.is_comment():
            # コメント有り
            if "対抗" in comment_separator.comment:
                new_comment = f'{comment_separator.comment}'
            else:
                new_comment = f'対抗{comment_separator.comment}'
        else:
            # コメント無し
            new_comment = "対抗ロール"
        comment_separator.set_comment(new_comment)

        comparison_separator = self.get_comparison_separator().separate(comment_separator.command_line)
        #print(comparison_separator.comparison_name)
        #print(comparison_separator.comparison_value)
        command_string = comparison_separator.dice_command

        command_line = command_string.split(" ")
        removal_blank = [word.strip() for word in command_line if word.strip() != ""]
        #print("removal_blank: " + str(removal_blank))

        if not len(removal_blank) >= 2:
            raise InvalidFormulaException()

        active_side = int(self.execute_eval(removal_blank[0]))
        passive_side = int(self.execute_eval(removal_blank[1]))

        name = f"{active_side}vs{passive_side}"
        value = 50 + ((active_side - passive_side) * 5)

        comparison_separator.set_dice_command("1d100")
        comparison_separator.set_conditional_expression("<=")
        comparison_separator.set_comparison_name(name)
        comparison_separator.set_comparison_value(value)

        return self.dice_command_roll()
