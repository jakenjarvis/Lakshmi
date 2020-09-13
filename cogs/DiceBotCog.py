#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from discord.ext import commands

import mojimoji

import LakshmiErrors
import MultilineBot
from contents.dice.DiceCommandProcessor import InvalidFormulaException, ArgumentOutOfRangeException, InvalidCharacterException
from contents.dice.CallOfCthulhuDice import CallOfCthulhuDice
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

            comment_separator = dice.get_comment_separator().separate(command)
            #print(comment_separator.command_line)
            #print(comment_separator.comment)

            comparison_separator = dice.get_comparison_separator().separate(comment_separator.command_line)
            #print(comparison_separator.comparison_name)
            #print(comparison_separator.comparison_value)

            command_string = comparison_separator.dice_command
            print(f"command_string: {command_string}")

            name = ""
            value = 0

            # 文字列指定
            # アクティブキャラのスキルあいまい検索
            find_string = mojimoji.han_to_zen(command_string)
            items = search_skills.search(find_string)
            if len(items) >= 1:
                # 該当スキルが見つかった。
                search_result: SearchResult = items[0]
                if len(search_result.sub_name) >= 1:
                    pickskillname = f"{search_result.main_name}({search_result.sub_name})"
                else:
                    pickskillname = f"{search_result.main_name}"

                name = pickskillname
                value = search_skills.get_skill_value(search_result.link_name)

                stock.append(f"…ん。{character.character_name}さんのスキル `{pickskillname}` は `{value}` よ……。")
            else:
                name = command_string
                value = int(dice.execute_eval(command_string))

            comparison_separator.set_dice_command("1d100")
            comparison_separator.set_conditional_expression("<=")
            comparison_separator.set_comparison_name(name)
            comparison_separator.set_comparison_value(value)

            roll_result = dice.dice_command_roll()
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
