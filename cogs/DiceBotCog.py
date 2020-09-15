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
from ChoiceReactionFlow import ChoiceReactionFlow

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

    @commands.command()
    async def sp(self, context: commands.Context):
        """アクティブキャラのスキルを参照して選択したダイスを振ります。(skill percent)"""
        # SAN:😱　アイデア:💡　幸運:🍀　知識:🧠　聞き耳:👂　図書館:📚　目星:👀
        stock = []
        #TODO: DiscordのMAXは20だった。
        # max 30
        master_emojis = [
            "0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣",
            "☮️", "✝️", "☪️", "🕉", "☸️", "✡️", "☯️", "☦️", "♈️", "♉️",
            "♊️", "♋️", "♌️", "♍️", "♎️", "♏️", "♐️", "♑️", "♒️", "♓️",
            "😱","💡","🍀","🧠","👂","📚","👀",
            ]
        used_emojis = []
        keywords = {}
        database = []
        emoji_index = 0

        author_name = str(context.author.name)
        display_name = str(context.author.display_name)

        character = await self.manager.get_character_information(context, "")

        # 陳列するスキルの一覧を作成する。
        def add_item(keyword, skill_name, skill_value, emoji, display):
            data = {
                "keyword" : str(keyword),
                "skill_name" : str(skill_name),
                "skill_value" : str(skill_value),
                "emoji" : str(emoji),
                "display" : str(display),
            }
            keywords[str(keyword)] = data
            database.append(data)
            used_emojis.append(emoji)

        def add_skills(target, keyword, emoji):
            add_item(keyword,
                target[keyword].get_fullname(),
                f"{target[keyword].current}",
                emoji,
                target[keyword].to_display_string()
                )

        # 固定アイテム
        add_item("sanity_points", "SAN", f"{character.sanity_points.current}", "😱", f"SAN: {character.sanity_points.current}")
        add_skills(character.characteristics, "idea", "💡")
        add_skills(character.characteristics, "luck", "🍀")
        add_skills(character.characteristics, "knowledge", "🧠")
        add_skills(character.search_skills, "listen", "👂")
        add_skills(character.search_skills, "library_use", "📚")
        add_skills(character.search_skills, "spot_hidden", "👀")

        targets = [character.combat_skills, character.search_skills, character.behavioral_skills, character.negotiation_skills, character.knowledge_skills]
        for target in targets:
            for key in target.keys():
                if target[key].base != target[key].current:
                    if not key in keywords:
                        pick_emoji = master_emojis[emoji_index]
                        add_skills(target, key, pick_emoji)
                        emoji_index += 1

        first_send = f""
        first_send += f"…ん。{character.character_name}さんの、どのスキルでダイスを振るのか決めて……。"
        first_send += f"\n"
        #first_send += f"```"
        for data in database:
            first_send += f"{data['emoji']} {data['display']}　"
        #first_send += f"```"
        first_send += f"\n"
        first_send += f"どのスキルにするの？…… `30秒以内` に選んで頂戴……。"

        bot_message = await context.send(first_send) # ここでself.bot.sendは使えない。

        flow = ChoiceReactionFlow(self.bot, context)
        flow.set_target_message(bot_message, used_emojis)

        emoji = await flow.wait_for_choice_reaction(timeout=30)
        if emoji:
            chosed_index = used_emojis.index(emoji)
            chosed_data = database[chosed_index]
            skill_name = chosed_data["skill_name"]
            skill_value = chosed_data["skill_value"]

            stock.append(f"…お。{skill_name}ね？ダイスを振るわよ……。")
            await self.bot.send("\n".join(stock))

            p_command = f"{skill_value} #{emoji}{skill_name}"
            print(f"p_command: {p_command}")
            await self.p(context, command=p_command)
        else:
            stock.append(f'時間切れよ………{context.author.display_name}さんは優柔不断ね……。')
            await self.bot.send("\n".join(stock))

def setup(bot):
    bot.add_cog(DiceBotCog(bot))
