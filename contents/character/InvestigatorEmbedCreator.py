#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import result
import discord
import itertools

from contents.character.Investigator import Investigator, SkillSet

class InvestigatorEmbedCreator():
    @staticmethod
    def __create_information_embed(char: Investigator, is_summarize_backstory: bool) -> discord.Embed:
        backstory = ""
        if is_summarize_backstory:
            backstory = char.backstory.splitlines()[0]
        else:
            backstory = char.backstory

        lst = "💀" if char.lost else ""

        result = discord.Embed(
            title=f"{lst}{char.character_name} - `{char.occupation}` - `{char.sex}({char.age}歳)`",
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
    def __create_omitted_embed(char: Investigator) -> discord.Embed:
        lst = "💀" if char.lost else ""

        result = discord.Embed()
        result.set_author(
            name=f"{lst}{char.character_name} - {char.occupation} - {char.sex}({char.age}歳)",
            url=f"{char.site_url}",
            icon_url=char.image_url
            )

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
        if char.lost:
            out_value += f"`<ロスト>`　"
        result.add_field(name="探索者付随情報", value=out_value, inline=False)

    @staticmethod
    def __append_current_san_value(result: discord.Embed, char: Investigator):
        # 現在SAN値
        out_value = f"{char.sanity_points.current} / {char.sanity_points.max_insane}　(不定領域: {char.sanity_points.indef_insane})"
        result.add_field(name="現在SAN値", value=out_value, inline=False)

    @staticmethod
    def __append_characteristics(result: discord.Embed, char: Investigator, is_omitted_characteristics: bool):
        # 特性
        if is_omitted_characteristics:
            abilitys = ["strength", "constitution", "power", "dexterity", "appearance", "size", "intelligence", "education", "idea", "luck", "knowledge"]
        else:
            abilitys = char.characteristics.keys()

        out_value = f""
        for key in abilitys:
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
        out_value = out_value if len(out_value) >= 1 else "無し"
        out_title = f"戦闘技能 `[初期値除外]`" if is_change_from_initial_value else f"戦闘技能"
        result.add_field(name=out_title, value=out_value, inline=False)

        # 探索技能
        out_value = f""
        for key in char.search_skills.keys():
            skillset = char.search_skills[key]
            out_value += InvestigatorEmbedCreator.__create_skillset_string(skillset, is_change_from_initial_value)
        out_value = out_value if len(out_value) >= 1 else "無し"
        out_title = f"探索技能 `[初期値除外]`" if is_change_from_initial_value else f"探索技能"
        result.add_field(name=out_title, value=out_value, inline=False)

        # 行動技能
        out_value = f""
        for key in char.behavioral_skills.keys():
            skillset = char.behavioral_skills[key]
            out_value += InvestigatorEmbedCreator.__create_skillset_string(skillset, is_change_from_initial_value)
        out_value = out_value if len(out_value) >= 1 else "無し"
        out_title = f"行動技能 `[初期値除外]`" if is_change_from_initial_value else f"行動技能"
        result.add_field(name=out_title, value=out_value, inline=False)

        # 交渉技能
        out_value = f""
        for key in char.negotiation_skills.keys():
            skillset = char.negotiation_skills[key]
            out_value += InvestigatorEmbedCreator.__create_skillset_string(skillset, is_change_from_initial_value)
        out_value = out_value if len(out_value) >= 1 else "無し"
        out_title = f"交渉技能 `[初期値除外]`" if is_change_from_initial_value else f"交渉技能"
        result.add_field(name=out_title, value=out_value, inline=False)

        # 知識技能
        out_value = f""
        for key in char.knowledge_skills.keys():
            skillset = char.knowledge_skills[key]
            out_value += InvestigatorEmbedCreator.__create_skillset_string(skillset, is_change_from_initial_value)
        out_value = out_value if len(out_value) >= 1 else "無し"
        out_title = f"知識技能 `[初期値除外]`" if is_change_from_initial_value else f"知識技能"
        result.add_field(name=out_title, value=out_value, inline=False)

    @staticmethod
    def create_full_status(char: Investigator) -> discord.Embed:
        is_summarize_backstory = True
        is_change_from_initial_value = False
        is_omitted_characteristics = False

        result = InvestigatorEmbedCreator.__create_information_embed(char, is_summarize_backstory)

        # 探索者付随情報
        InvestigatorEmbedCreator.__append_info_associated_with_investigator(result, char)
        # 現在SAN値
        InvestigatorEmbedCreator.__append_current_san_value(result, char)
        # 特性
        InvestigatorEmbedCreator.__append_characteristics(result, char, is_omitted_characteristics)
        # スキル
        InvestigatorEmbedCreator.__append_skills(result, char, is_change_from_initial_value)

        return result

    @staticmethod
    def create_short_status(char: Investigator) -> discord.Embed:
        is_summarize_backstory = True
        is_change_from_initial_value = True
        is_omitted_characteristics = False

        result = InvestigatorEmbedCreator.__create_information_embed(char, is_summarize_backstory)

        # 探索者付随情報
        InvestigatorEmbedCreator.__append_info_associated_with_investigator(result, char)
        # 現在SAN値
        InvestigatorEmbedCreator.__append_current_san_value(result, char)
        # 特性
        InvestigatorEmbedCreator.__append_characteristics(result, char, is_omitted_characteristics)
        # スキル
        InvestigatorEmbedCreator.__append_skills(result, char, is_change_from_initial_value)

        return result

    @staticmethod
    def create_backstory_status(char: Investigator) -> discord.Embed:
        is_summarize_backstory = False
        is_change_from_initial_value = True
        is_omitted_characteristics = False

        result = InvestigatorEmbedCreator.__create_information_embed(char, is_summarize_backstory)

        # 探索者付随情報
        InvestigatorEmbedCreator.__append_info_associated_with_investigator(result, char)

        return result

    @staticmethod
    def create_omitted_status(char: Investigator) -> discord.Embed:
        is_summarize_backstory = False
        is_change_from_initial_value = True
        is_omitted_characteristics = True

        result = InvestigatorEmbedCreator.__create_omitted_embed(char)

        # 現在SAN値
        InvestigatorEmbedCreator.__append_current_san_value(result, char)
        # 特性(省略系)
        InvestigatorEmbedCreator.__append_characteristics(result, char, is_omitted_characteristics)
        # スキル
        InvestigatorEmbedCreator.__append_skills(result, char, is_change_from_initial_value)

        return result
