#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple, Pattern, Match, Type

from discord.ext import commands

import mojimoji

import LakshmiErrors
from contents.dice.DiceCommandProcessor import InvalidFormulaException, ArgumentOutOfRangeException, InvalidCharacterException
from contents.dice.CallOfCthulhuDice import CallOfCthulhuDice
from contents.dice.SkillNameReplacer import SkillNameReplacer
from contents.FuzzySearchInvestigatorSkills import FuzzySearchInvestigatorSkills, SearchResult
from contents.character.CharacterManager import CharacterManager

class DiceBotCog(commands.Cog, name='ダイス系'):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage
        self.manager = CharacterManager(self.bot)

    @commands.command()
    async def r(self, context: commands.Context, *, command: str):
        """アクティブキャラのスキルを参照してダイスを振ります。(roll)"""
        stock = []
        stock.append(f'{context.author.mention}')

        await context.trigger_typing()

        author_name = str(context.author.name)
        display_name = str(context.author.display_name)

        character = await self.manager.get_character_information(context, "")
        search_skills = FuzzySearchInvestigatorSkills(character)

        try:
            dice = CallOfCthulhuDice()
            dice.append_replacer_types(SkillNameReplacer,
                bot=self.bot,
                manager=self.manager,
                character=character,
                search_skills=search_skills,
                processor=dice,
                )

            dice.comment_separator.separate(command)

            skill_name_command = dice.comment_separator.expression_formula
            new_command = f"1d100<={skill_name_command}"
            dice.comment_separator.expression_formula = new_command

            dice.execute_evaluation_expression()
            dice.execute_replacers()
            dice.execute_calculate()

            skill_name_replacers: List[SkillNameReplacer] = dice.find_replacers(SkillNameReplacer)
            for replacer in skill_name_replacers:
                if len(replacer.skill_name) >= 1:
                    stock.append(f"…ん。{character.character_name}さんのスキル `{replacer.skill_name}` は `{replacer.skill_value}` よ……。")

            roll_result = dice.generate_dice_result_string()
            stock.append(f'{roll_result}')

        except InvalidFormulaException as e:
            raise commands.CommandNotFound
        except ArgumentOutOfRangeException as e:
            raise LakshmiErrors.ArgumentOutOfRangeException
        except InvalidCharacterException as e:
            raise commands.CommandNotFound

        await self.bot.send("\n".join(stock))

    @commands.command()
    async def p(self, context: commands.Context, *, command: str):
        """1d100固定のパーセント指定でダイスを振ります。(percent)"""
        stock = []
        stock.append(f'{context.author.mention}')

        result = ""
        try:
            result = CallOfCthulhuDice().percent(command)
        except InvalidFormulaException as e:
            raise commands.CommandNotFound
        except ArgumentOutOfRangeException as e:
            raise LakshmiErrors.ArgumentOutOfRangeException
        except InvalidCharacterException as e:
            raise commands.CommandNotFound

        stock.append(f'{result}')
        await self.bot.send("\n".join(stock))

    @commands.command()
    async def vs(self, context: commands.Context, *, command: str):
        """対抗ロールでダイスを振ります。(versus)"""
        stock = []
        stock.append(f'{context.author.mention}')

        result = ""
        try:
            result = CallOfCthulhuDice().versus(command)
        except InvalidFormulaException as e:
            raise commands.CommandNotFound
        except ArgumentOutOfRangeException as e:
            raise LakshmiErrors.ArgumentOutOfRangeException
        except InvalidCharacterException as e:
            raise commands.CommandNotFound

        stock.append(f'{result}')
        await self.bot.send("\n".join(stock))

    @commands.command()
    async def f(self, context: commands.Context, *, command: str):
        """mDn形式で面を指定してダイスを振ります。(fate)"""
        stock = []
        stock.append(f'{context.author.mention}')

        result = ""
        try:
            result = CallOfCthulhuDice().roll(command)
        except InvalidFormulaException as e:
            raise commands.CommandNotFound
        except ArgumentOutOfRangeException as e:
            raise LakshmiErrors.ArgumentOutOfRangeException
        except InvalidCharacterException as e:
            raise commands.CommandNotFound

        stock.append(f'{result}')
        await self.bot.send("\n".join(stock))

    @commands.command()
    async def sf(self, context: commands.Context, *, command: str):
        """fと同じ。結果をDMで通知します。(secret fate)"""
        stock = []
        # メッセージの組み立て NOTE: DMするのでメンションは付けない
        #stock.append(f'{context.author.mention}')
        result = ""
        try:
            result = CallOfCthulhuDice().roll(command)
        except InvalidFormulaException as e:
            raise commands.CommandNotFound
        except ArgumentOutOfRangeException as e:
            raise LakshmiErrors.ArgumentOutOfRangeException
        except InvalidCharacterException as e:
            raise commands.CommandNotFound

        stock.append(f'{result}')
        await self.bot.author.send("\n".join(stock))

def setup(bot):
    bot.add_cog(DiceBotCog(bot))
