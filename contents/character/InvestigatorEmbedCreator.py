#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import result
import discord

from contents.character.Investigator import Investigator
from contents.character.CharacterVampireBloodNetGetter import CharacterVampireBloodNetGetter

class InvestigatorEmbedCreator():
    @staticmethod
    def create_full_status(char: Investigator) -> discord.Embed:
        onelinebackstory = char.backstory.splitlines()[0]

        result = discord.Embed(
            title=f"{char.name} - `{char.occupation}` - `{char.sex}({char.age}歳)`",
            description=f"{onelinebackstory}"
            )
        result.set_author(
            name=f"{char.site_name}",
            url=f"{char.site_url}",
            icon_url=char.site_favicon_url
            )
        result.set_thumbnail(
            url="https://cdn.discordapp.com/embed/avatars/0.png"
            )

        # 探索者付随情報
        out_value = f""
        if len(char.tag) >= 1:
            out_value += f"**TAG:**　`{char.tag.replace(' ','`　`')}`"
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
        result.add_field(name="探索者付随情報", value=out_value, inline=False)

        # 現在SAN値
        out_value = f"{char.sanity_points.current} / {char.sanity_points.max_insane}　(不定領域: {char.sanity_points.indef_insane})"
        result.add_field(name="現在SAN値", value=out_value, inline=False)

        # 基礎能力、特性等
        out_value = f""
        for ability in char.characteristics.category_all_keys():
            out_value += f"{ability.to_display_string()}　"
        result.add_field(name="特性", value=out_value, inline=False)

        #out_value = f""
        #for ability in char.characteristics.category1_keys():
        #    out_value += f"`{ability.to_display_string()}`　"
        #result.add_field(name="能力値", value=out_value, inline=False)

        #out_value = f""
        #out_value += f"\n"
        #for ability in char.characteristics.category2_keys():
        #    out_value += f"`{ability.to_display_string()}`　"
        #result.add_field(name="特性", value=out_value, inline=False)

        # 戦闘技能
        out_value = f""
        for key in char.combat_skills.keys():
            out_value += f"{char.combat_skills[key].to_display_string()}　"
        result.add_field(name="戦闘技能", value=out_value, inline=False)

        # 探索技能
        out_value = f""
        for key in char.search_skills.keys():
            out_value += f"{char.search_skills[key].to_display_string()}　"
        result.add_field(name="探索技能", value=out_value, inline=False)

        # 行動技能
        out_value = f""
        for key in char.behavioral_skills.keys():
            out_value += f"{char.behavioral_skills[key].to_display_string()}　"
        result.add_field(name="行動技能", value=out_value, inline=False)

        # 交渉技能
        out_value = f""
        for key in char.negotiation_skills.keys():
            out_value += f"{char.negotiation_skills[key].to_display_string()}　"
        result.add_field(name="交渉技能", value=out_value, inline=False)

        # 知識技能
        out_value = f""
        for key in char.knowledge_skills.keys():
            out_value += f"{char.knowledge_skills[key].to_display_string()}　"
        result.add_field(name="知識技能", value=out_value, inline=False)

        return result
