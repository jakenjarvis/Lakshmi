#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import result
import discord

from contents.CharacterVampireBloodNetGetter import CharacterVampireBloodNetGetter
from contents.Investigator import Investigator

class InvestigatorEmbedCreator():
    @staticmethod
    def create(char: Investigator) -> discord.Embed:
        onelinebackstory = char.backstory.splitlines()[0]

        result = discord.Embed(
            title=f"{char.name} - `{char.occupation}`　`{char.sex}({char.age}歳)`",
            description=f"{onelinebackstory}"
            )
        result.set_author(
            name=f"{char.name}",
            url=f"{char.site_url}",
            icon_url="https://cdn.discordapp.com/embed/avatars/0.png"
            )
        result.set_thumbnail(
            url="https://cdn.discordapp.com/embed/avatars/0.png"
            )

        # その他情報
        out_value = f""
        if len(char.tag) >= 1:
            out_value += f"**TAG:** `{char.tag.replace(' ','`　`')}`"
            out_value += f"\n"
        if len(char.personal_data.height.strip()) >= 1:
            out_value += f"`身長: {char.personal_data.height}`　"
        if len(char.personal_data.weight.strip()) >= 1:
            out_value += f"`体重: {char.personal_data.weight}`　"
        if len(char.personal_data.hair_color.strip()) >= 1:
            out_value += f"`髪の色: {char.personal_data.hair_color}`　"
        if len(char.personal_data.eye_color.strip()) >= 1:
            out_value += f"`瞳の色: {char.personal_data.eye_color}`　"
        if len(char.personal_data.skin_color.strip()) >= 1:
            out_value += f"`肌の色: {char.personal_data.skin_color}`　"
        result.add_field(name="その他情報", value=out_value, inline=False)

        # 基礎能力、特性等
        out_value = f"STR: {char.STR}　CON: {char.CON}　POW: {char.POW}　DEX: {char.DEX}　APP: {char.APP}　SIZ: {char.SIZ}　INT: {char.INT}　EDU: {char.EDU}"
        result.add_field(name="能力値", value=out_value, inline=False)
        out_value = f"HP: {char.HP}　MP: {char.MP}　SAN値: {char.SAN}　アイデア: {char.IDEA}　幸運: {char.LUCK}　知識: {char.KNOWLEDGE}"
        result.add_field(name="特性", value=out_value, inline=False)

        # 戦闘技能
        out_value = f""
        for key in char.combat_skills.keys():
            if len(char.combat_skills[key].skill_subname) >= 1:
                out_value += f"{char.combat_skills[key].skill_name}({char.combat_skills[key].skill_subname}): {char.combat_skills[key].current}　"
            else:
                out_value += f"{char.combat_skills[key].skill_name}: {char.combat_skills[key].current}　"
        result.add_field(name="戦闘技能", value=out_value, inline=False)

        # 探索技能
        out_value = f""
        for key in char.search_skills.keys():
            if len(char.search_skills[key].skill_subname) >= 1:
                out_value += f"{char.search_skills[key].skill_name}({char.search_skills[key].skill_subname}): {char.search_skills[key].current}　"
            else:
                out_value += f"{char.search_skills[key].skill_name}: {char.search_skills[key].current}　"
        result.add_field(name="探索技能", value=out_value, inline=False)

        # 行動技能
        out_value = f""
        for key in char.behavioral_skills.keys():
            if len(char.behavioral_skills[key].skill_subname) >= 1:
                out_value += f"{char.behavioral_skills[key].skill_name}({char.behavioral_skills[key].skill_subname}): {char.behavioral_skills[key].current}　"
            else:
                out_value += f"{char.behavioral_skills[key].skill_name}: {char.behavioral_skills[key].current}　"
        result.add_field(name="行動技能", value=out_value, inline=False)

        # 交渉技能
        out_value = f""
        for key in char.negotiation_skills.keys():
            if len(char.negotiation_skills[key].skill_subname) >= 1:
                out_value += f"{char.negotiation_skills[key].skill_name}({char.negotiation_skills[key].skill_subname}): {char.negotiation_skills[key].current}　"
            else:
                out_value += f"{char.negotiation_skills[key].skill_name}: {char.negotiation_skills[key].current}　"
        result.add_field(name="交渉技能", value=out_value, inline=False)

        # 知識技能
        out_value = f""
        for key in char.knowledge_skills.keys():
            if len(char.knowledge_skills[key].skill_subname) >= 1:
                out_value += f"{char.knowledge_skills[key].skill_name}({char.knowledge_skills[key].skill_subname}): {char.knowledge_skills[key].current}　"
            else:
                out_value += f"{char.knowledge_skills[key].skill_name}: {char.knowledge_skills[key].current}　"
        result.add_field(name="知識技能", value=out_value, inline=False)

        return result
