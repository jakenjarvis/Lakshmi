#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple, Pattern, Match, Type

from discord.ext import commands

import LakshmiErrors
from contents.dice.DiceCommandProcessor import InvalidFormulaException, ArgumentOutOfRangeException, InvalidCharacterException
from contents.dice.CallOfCthulhuDice import CallOfCthulhuDice
from contents.dice.DiceCommandProcessor import DiceCommandProcessor, ReplacerBase, EvaluationExpressionSeparator, InvalidFormulaException, FormulaSeparator, CalculatorBase

from contents.character.Investigator import Investigator
from contents.character.CharacterManager import CharacterManager
from contents.FuzzySearchInvestigatorSkills import FuzzySearchInvestigatorSkills, SearchResult

class SkillNameReplacer(ReplacerBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bot: commands.Bot = kwargs["bot"]
        self.manager: CharacterManager = kwargs["manager"]
        self.character: Investigator = kwargs["character"]
        self.search_skills: FuzzySearchInvestigatorSkills = kwargs["search_skills"]
        self.processor: CallOfCthulhuDice = kwargs["processor"]

        self.search_results: List[SearchResult] = []

        self.skill_name = ""
        self.skill_value = 0

    # overwride
    def replace_comparison_operator(self, separator: EvaluationExpressionSeparator):
        return self

    # overwride
    def replace_formula(self, separator: FormulaSeparator):
        if len(separator.calculation_formula_center) >= 1:
            command_string = separator.calculation_formula_center

            self.search_results = self.search_skills.search(command_string)
            if len(self.search_results) >= 1:
                # 該当スキルが見つかった。
                search_result: SearchResult = self.search_results[0]
                if len(search_result.sub_name) >= 1:
                    pickskillname = f"{search_result.main_name}({search_result.sub_name})"
                else:
                    pickskillname = f"{search_result.main_name}"

                self.skill_name = pickskillname
                self.skill_value = self.search_skills.get_skill_value(search_result.link_name)
            else:
                calculator = CalculatorBase()
                self.skill_name = command_string
                self.skill_value = int(calculator.execute_eval(command_string))

            separator.calculation_formula_center = f"({self.skill_value})"
            separator.display_formula_center = f"({self.skill_name}:{self.skill_value})"
        return self

