#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import result
import discord

from contents.character.Investigator import Investigator, SkillSet
from contents.character.CharacterVampireBloodNetGetter import CharacterVampireBloodNetGetter

class InvestigatorEmbedCreator():

    @staticmethod
    def __create_embed(char: Investigator, is_summarize_backstory: bool) -> discord.Embed:
        backstory = ""
        if is_summarize_backstory:
            backstory = char.backstory.splitlines()[0]
        else:
            backstory = char.backstory

        result = discord.Embed(
            title=f"{char.character_name} - `{char.occupation}` - `{char.sex}({char.age}歳)`",
            description=f"{backstory}"
            )
        result.set_author(
            name=f"{char.site_name}",
            url=f"{char.site_url}",
            icon_url=char.site_favicon_url
            )

        if len(char.image_url) >= 1:
            result.set_thumbnail(url=char.image_url)

        return result

    @staticmethod
    def __append_info_associated_with_investigator(result: discord.Embed, char: Investigator):
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

    @staticmethod
    def __append_current_san_value(result: discord.Embed, char: Investigator):
        # 現在SAN値
        out_value = f"{char.sanity_points.current} / {char.sanity_points.max_insane}　(不定領域: {char.sanity_points.indef_insane})"
        result.add_field(name="現在SAN値", value=out_value, inline=False)

    @staticmethod
    def __append_characteristics(result: discord.Embed, char: Investigator):
        # 特性
        out_value = f""
        for key in char.characteristics.keys():
            out_value += f"{char.characteristics[key].to_display_string()}　"
        result.add_field(name="特性", value=out_value, inline=False)

    @staticmethod
    def __create_skillset_string(skillset: SkillSet, is_change_from_initial_value: bool):
        result = ""
        if is_change_from_initial_value:
            if skillset.base != skillset.current:
                result = f"{skillset.to_display_string()}　"
        else:
            result = f"{skillset.to_display_string()}　"
        return result

    @staticmethod
    def __append_skills(result: discord.Embed, char: Investigator, is_change_from_initial_value: bool):
        # 戦闘技能
        out_value = f""
        for key in char.combat_skills.keys():
            skillset = char.combat_skills[key]
            out_value += InvestigatorEmbedCreator.__create_skillset_string(skillset, is_change_from_initial_value)
        result.add_field(name="戦闘技能", value=out_value, inline=False)

        # 探索技能
        out_value = f""
        for key in char.search_skills.keys():
            skillset = char.search_skills[key]
            out_value += InvestigatorEmbedCreator.__create_skillset_string(skillset, is_change_from_initial_value)
        result.add_field(name="探索技能", value=out_value, inline=False)

        # 行動技能
        out_value = f""
        for key in char.behavioral_skills.keys():
            skillset = char.behavioral_skills[key]
            out_value += InvestigatorEmbedCreator.__create_skillset_string(skillset, is_change_from_initial_value)
        result.add_field(name="行動技能", value=out_value, inline=False)

        # 交渉技能
        out_value = f""
        for key in char.negotiation_skills.keys():
            skillset = char.negotiation_skills[key]
            out_value += InvestigatorEmbedCreator.__create_skillset_string(skillset, is_change_from_initial_value)
        result.add_field(name="交渉技能", value=out_value, inline=False)

        # 知識技能
        out_value = f""
        for key in char.knowledge_skills.keys():
            skillset = char.knowledge_skills[key]
            out_value += InvestigatorEmbedCreator.__create_skillset_string(skillset, is_change_from_initial_value)
        result.add_field(name="知識技能", value=out_value, inline=False)

    @staticmethod
    def create_full_status(char: Investigator) -> discord.Embed:
        is_summarize_backstory = True
        is_change_from_initial_value = False
 
        result = InvestigatorEmbedCreator.__create_embed(char, is_summarize_backstory)

        # 探索者付随情報
        InvestigatorEmbedCreator.__append_info_associated_with_investigator(result, char)
        # 現在SAN値
        InvestigatorEmbedCreator.__append_current_san_value(result, char)
        # 特性
        InvestigatorEmbedCreator.__append_characteristics(result, char)
        # スキル
        InvestigatorEmbedCreator.__append_skills(result, char, is_change_from_initial_value)

        return result

    @staticmethod
    def create_short_status(char: Investigator) -> discord.Embed:
        is_summarize_backstory = True
        is_change_from_initial_value = True
 
        result = InvestigatorEmbedCreator.__create_embed(char, is_summarize_backstory)

        # 探索者付随情報
        InvestigatorEmbedCreator.__append_info_associated_with_investigator(result, char)
        # 現在SAN値
        InvestigatorEmbedCreator.__append_current_san_value(result, char)
        # 特性
        InvestigatorEmbedCreator.__append_characteristics(result, char)
        # スキル
        InvestigatorEmbedCreator.__append_skills(result, char, is_change_from_initial_value)

        return result

    @staticmethod
    def create_backstory_status(char: Investigator) -> discord.Embed:
        is_summarize_backstory = False
 
        result = InvestigatorEmbedCreator.__create_embed(char, is_summarize_backstory)

        # 探索者付随情報
        InvestigatorEmbedCreator.__append_info_associated_with_investigator(result, char)

        return result
