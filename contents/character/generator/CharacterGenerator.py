#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple
import re
import math
import random
import copy
from collections import OrderedDict

import ulid

from contents.character.Investigator import Investigator, SkillSet, InitialValueOfSkills
from contents.character.generator.CharacterOccupation import CharacterOccupation
from contents.character.generator.CharacterPersonality import CharacterPersonality
from contents.character.generator.CharacterBloodType import CharacterBloodType
from contents.character.generator.PriorityRandomChooser import PriorityRandomChooser
from contents.character.generator.SkillPointDistributor import SkillPointDistributor
from contents.character.generator.CharacterAppearance import CharacterAppearance
from contents.character.generator.GeneratedSkill import GeneratedSkill

from contents.character.generator.ParameterComplementary import ParameterComplementary

class CharacterGenerator():
    def __init__(self):
        self.investigator: Investigator = Investigator()

    def dice(self, number: int, surface: int) -> int:
        return sum(random.randint(1, surface) for _ in range(number))

    def find_skillset(self, key: str) -> SkillSet:
        result: SkillSet = None
        skills = [
            self.investigator.combat_skills,
            self.investigator.search_skills,
            self.investigator.behavioral_skills,
            self.investigator.negotiation_skills,
            self.investigator.knowledge_skills
        ]
        for skill in skills:
            if key in skill.keys():
                result = skill[key]
        return result

    def register_skillset(self, key: str) -> SkillSet:
        result: SkillSet = None
        initializer = InitialValueOfSkills(self.investigator.DEX, self.investigator.EDU)
        # TODO: 新規スキルを登録するにはデータが必要。とりあえず「その他の言語」のみ
        if key == "other_language":
            result = SkillSet("その他の言語", "") # TODO: サブは後で入れる？
            result.base = initializer.get_value(key)
            result.calculate()
            self.investigator.negotiation_skills["other_language"] = result
        else:
            raise Exception
        return result

    def generate(self, parameter: ParameterComplementary):
        # TODO: パラメータチェック
        # TODO: age <= 11 はエラーとする。

        # 能力値
        self.investigator.characteristics["strength"].set_initial_value(self.dice(3, 6))
        self.investigator.characteristics["constitution"].set_initial_value(self.dice(3, 6))
        self.investigator.characteristics["power"].set_initial_value(self.dice(3, 6))
        self.investigator.characteristics["dexterity"].set_initial_value(self.dice(3, 6))
        self.investigator.characteristics["appearance"].set_initial_value(self.dice(3, 6))
        self.investigator.characteristics["size"].set_initial_value(self.dice(2, 6) + 6)
        self.investigator.characteristics["intelligence"].set_initial_value(self.dice(2, 6) + 6)
        self.investigator.characteristics["education"].set_initial_value(self.dice(3, 6) + 3)
        #self.investigator.characteristics["hit_points"].set_initial_value(math.ceil((self.investigator.CON + self.investigator.SIZ) / 2))
        #self.investigator.characteristics["magic_points"].set_initial_value(self.investigator.POW)
        #self.investigator.characteristics["initial_sanity"].set_initial_value(self.investigator.POW * 5)
        #self.investigator.characteristics["idea"].set_initial_value(self.investigator.INT * 5)
        #self.investigator.characteristics["luck"].set_initial_value(self.investigator.POW * 5)
        #self.investigator.characteristics["knowledge"].set_initial_value(self.investigator.EDU * 5)

        self.investigator.calculate()

        # 年齢による能力値の増減修正
        self.set_age_correction(parameter.age)

        self.investigator.calculate()

        # SAN値
        self.investigator.sanity_points.current = self.investigator.SAN
        #self.investigator.sanity_points.max_insane
        #self.investigator.sanity_points.indef_insane

        # 技能
        #self.investigator.skill_points.remaining_occupation                                 # 残り職業ポイント
        #self.investigator.skill_points.remaining_interest                                   # 残り興味ポイント
        #self.investigator.skill_points.max_occupation = self.investigator.EDU * 20          # 最大職業ポイント
        #self.investigator.skill_points.max_interest = self.investigator.INT * 10            # 最大興味ポイント
        self.investigator.skill_points.additions_occupation = 0                             # 追加職業ポイント
        self.investigator.skill_points.additions_interest = 0                               # 追加興味ポイント

        self.investigator.calculate()


        # 血液型
        self.bloodtype = CharacterBloodType()
        # 性格
        self.personality = CharacterPersonality()
        # 職業
        self.occupation = CharacterOccupation(parameter.occupation)
        # 容姿
        self.appearance = CharacterAppearance()

        # 職業から性格を選択(その職業になるためにはそれなりの性格が必要と考える)
        self.personality.set_key(self.occupation.choice_personality(parameter.occupation))

        print("-----")
        print(f"{parameter.gender}, {parameter.age}歳, {parameter.occupation} : {self.occupation.get_name()}")
        print(f"blood_type_key: {self.bloodtype.get_key()} : {self.bloodtype.get_name()} : {self.bloodtype.get_description()}")
        print(f"personality_key: {self.personality.get_key()} : {self.personality.get_description()}")
        print("-----")

        # 取得スキル一時保持(選択したスキルの保持)
        self.occupation_skills: OrderedDict[str, GeneratedSkill] = OrderedDict() # 職業ポイント
        self.interest_skills: OrderedDict[str, GeneratedSkill] = OrderedDict()   # 興味ポイント

        # 重み付け率(性格別の重み)
        weighting_rate_for_occupation = self.personality.get_weighting_rate_for_occupation()
        weighting_rate_for_interest = self.personality.get_weighting_rate_for_interest()

        # 残スキル管理(血液型別に優先順位を準備し、選択したものを除外していく)
        self.skills_priority = self.bloodtype.get_skills_priority()
        chooser_occupation_skills = PriorityRandomChooser(self.skills_priority)
        chooser_interest_skills = PriorityRandomChooser(self.skills_priority)

        print(self.skills_priority)
        print("-----")

        # 職業P: 確定リストからスキルを選択する。
        for skill_key in self.occupation.get_confirmed_list():
            generated_skill = GeneratedSkill().set_definition(skill_key)
            generated_skill.set_reason_fixed_by_occupation()
            self.occupation_skills[generated_skill.skill_key] = generated_skill

            chooser_occupation_skills.chosen(generated_skill.skill_key)

        # 職業P: ２つ選択リストから優先順に選択する。
        priority_2_choice_skill_definitions = self.occupation.get_2_choice_skills()
        if len(priority_2_choice_skill_definitions) >= 1:
            original_key_list: Dict[str, GeneratedSkill] = {}
            new_list = []
            for skill_key in priority_2_choice_skill_definitions:
                generated_skill = GeneratedSkill().set_definition(skill_key)
                new_list.append(generated_skill.skill_key)
                original_key_list[generated_skill.skill_key] = generated_skill

            chooser_occupation_skills.set_narrowing_down_conditions(new_list)
            one_skill_key = chooser_occupation_skills.narrowing_down_choice_by_priority_weighting_rate(weighting_rate_for_occupation)
            two_skill_key = chooser_occupation_skills.narrowing_down_choice_by_priority_weighting_rate(weighting_rate_for_occupation)

            generated_skill = original_key_list[one_skill_key]
            generated_skill.set_reason_two_list_choice_by_occupation()
            self.occupation_skills[one_skill_key] = generated_skill

            generated_skill = original_key_list[two_skill_key]
            generated_skill.set_reason_two_list_choice_by_occupation()
            self.occupation_skills[two_skill_key] = generated_skill

            chooser_occupation_skills.set_narrowing_down_conditions()

        # 職業P: 残り１つ選択リストから優先順に選択する。
        choice_count = self.occupation.get_undetermined_skills()
        for _ in range(choice_count):
            skill_key = chooser_occupation_skills.choice_by_priority_weighting_rate(weighting_rate_for_occupation)

            generated_skill = GeneratedSkill().set_definition(skill_key)
            generated_skill.set_reason_one_free_choice_by_occupation()
            self.occupation_skills[generated_skill.skill_key] = generated_skill

        print("----- occupation_skills")
        for key, generated_skill in self.occupation_skills.items():
            print(f"{key}: {generated_skill.to_display_string()}")
        print("-----")

        self.investigator.calculate()

        # 職業スキルポイントの分配
        skills: List[str] = list(self.occupation_skills.keys())
        rate_function = self.personality.get_skill_distribution_rate_function_for_occupation()
        probabilitys: List[int] = rate_function(len(skills))

        current_values: List[int] = []
        for index, key in enumerate(skills):
            skillset: SkillSet = self.find_skillset(key)
            if skillset is None:
                skillset = self.register_skillset(key)
            current_values.append(skillset.current)

        distributor_occupation_skills = SkillPointDistributor(skills, probabilitys, current_values)
        distributor_occupation_skills.lottery(self.investigator.skill_points.remaining_occupation)

        for index, key in enumerate(skills):
            skillset: SkillSet = self.find_skillset(key)
            generated_skill = self.occupation_skills[key]
            if len(generated_skill.skill_subname) >= 1:
                skillset.skill_subname = generated_skill.skill_subname
            skillset.occupation = distributor_occupation_skills.get_value(key)

        self.investigator.calculate()

        # 趣味スキルポイントの分配
        interest_choices: Dict[str, int] = self.personality.get_number_of_interest_choices()
        duplicate_count: int = int(interest_choices["duplicate_count"])
        new_count: int = int(interest_choices["new_count"])

        # 取得した職業スキルと重複するスキルを個数分選択する。
        if duplicate_count >= 1:
            skills: List[str] = copy.deepcopy(list(self.occupation_skills.keys()))
            for index, key in enumerate(skills):
                skillset: SkillSet = self.find_skillset(key)
                # スキル値が既に85に到達しているものは除外する。
                if skillset.current >= 85:
                    skills.remove(key)

            chooser_interest_skills.set_narrowing_down_conditions(skills)

            for _ in range(duplicate_count):
                # MAX85に到達している場合などで足りなくなるケースがある。
                if chooser_interest_skills.is_choose_for_narrowing_down():
                    skill_key = chooser_interest_skills.narrowing_down_choice_by_priority_weighting_rate(weighting_rate_for_interest)

                    generated_skill = self.occupation_skills[skill_key]
                    #generated_skill.set_reason_free_choice_by_interest() # ここは重複セットしてしまうので上書きしない。
                    self.interest_skills[skill_key] = generated_skill
                else:
                    # 重複でスキルが選べなかった分は、新しく取得する
                    new_count += 1

            chooser_interest_skills.chosen_all_narrowing_down_conditions()

        # 取得していない新しいスキルを個数分選択する。
        if new_count >= 1:
            for _ in range(new_count):
                skill_key = chooser_interest_skills.choice_by_priority_weighting_rate(weighting_rate_for_interest)

                generated_skill = GeneratedSkill().set_definition(skill_key)
                generated_skill.set_reason_free_choice_by_interest()
                self.interest_skills[generated_skill.skill_key] = generated_skill

        print("----- interest_skills")
        for key, generated_skill in self.interest_skills.items():
            print(f"{key}: {generated_skill.to_display_string()}")
        print("-----")

        self.investigator.calculate()

        # 趣味スキルポイントの分配
        skills: List[str] = list(self.interest_skills.keys())
        rate_function = self.personality.get_skill_distribution_rate_function_for_interest()
        probabilitys: List[int] = rate_function(len(skills))

        current_values: List[int] = []
        for index, key in enumerate(skills):
            skillset: SkillSet = self.find_skillset(key)
            if skillset is None:
                skillset = self.register_skillset(key)
            current_values.append(skillset.current)

        distributor_interest_skills = SkillPointDistributor(skills, probabilitys, current_values)
        distributor_interest_skills.lottery(self.investigator.skill_points.remaining_interest)

        for index, key in enumerate(skills):
            skillset: SkillSet = self.find_skillset(key)
            generated_skill = self.interest_skills[key]
            if len(generated_skill.skill_subname) >= 1:
                skillset.skill_subname = generated_skill.skill_subname
            skillset.interest = distributor_interest_skills.get_value(key)

        # 母国語セット
        # スキルが振られていなくても、サブスキル名はセットする。
        if len(self.investigator.negotiation_skills["own_language"].skill_subname.strip()) == 0:
            generated_skill = GeneratedSkill().set_definition("own_language")
            self.investigator.negotiation_skills["own_language"].skill_subname = generated_skill.skill_subname

        self.investigator.calculate()

        # スキル構成文字列作成
        skill_composition_string = ""
        reason_fixed_by_occupations = []
        reason_two_list_choice_by_occupations = []
        reason_one_free_choice_by_occupations = []
        for key, generated_skill in self.occupation_skills.items():
            if generated_skill.reason_for_choosing == GeneratedSkill.REASON_FIXED_BY_OCCUPATION:
                skillset: SkillSet = self.find_skillset(generated_skill.skill_key)
                reason_fixed_by_occupations.append(skillset.get_fullname())
            if generated_skill.reason_for_choosing == GeneratedSkill.REASON_TWO_LIST_CHOICE_BY_OCCUPATION:
                skillset: SkillSet = self.find_skillset(generated_skill.skill_key)
                reason_two_list_choice_by_occupations.append(skillset.get_fullname())
            if generated_skill.reason_for_choosing == GeneratedSkill.REASON_ONE_FREE_CHOICE_BY_OCCUPATION:
                skillset: SkillSet = self.find_skillset(generated_skill.skill_key)
                reason_one_free_choice_by_occupations.append(skillset.get_fullname())
        if len(reason_fixed_by_occupations) >= 1:
            skill_composition_string += f"{'、'.join(reason_fixed_by_occupations)}"
        if len(reason_two_list_choice_by_occupations) >= 1:
            skill_composition_string += " ＋[ "
            skill_composition_string += f"{'、'.join(reason_two_list_choice_by_occupations)}"
            skill_composition_string += " ]"
        if len(reason_one_free_choice_by_occupations) >= 1:
            skill_composition_string += " ＋[ "
            skill_composition_string += f"{'、'.join(reason_one_free_choice_by_occupations)}"
            skill_composition_string += " ]"


        # 性別、年齢、職業
        self.investigator.unique_id = ulid.new()                                # Key
        self.investigator.site_id1 = ""                                         # SiteId1
        self.investigator.site_id2 = ""                                         # SiteId2
        self.investigator.site_url = ""                                         # SiteUrl
        self.investigator.site_name = "キャラクタ生成"                          # SiteName
        self.investigator.site_favicon_url = ""                                 # SiteFaviconUrl
        self.investigator.author_id = ""                                        # 所有者ID
        self.investigator.author_name = ""                                      # 所有者名
        self.investigator.active = False                                        # Active
        self.investigator.lost = False                                          # Lost
        self.investigator.tag = ""                                              # タグ ※後でセット
        self.investigator.image_url = ""                                        # 画像URL

        # パーソナルデータ
        self.investigator.personal_data.name = ""                               # 名前
        self.investigator.personal_data.occupation = self.occupation.get_name() # 職業
        self.investigator.personal_data.age = parameter.age                     # 年齢
        self.investigator.personal_data.sex = parameter.sex                     # 性別
        self.investigator.personal_data.residence = ""                          # 居住地
        self.investigator.personal_data.birthplace = "日本"                     # 出身地

        # 容姿計算(年齢セット後)
        self.appearance.calculate(self.investigator)

        self.investigator.personal_data.height = self.appearance.height         # 身長
        self.investigator.personal_data.weight = self.appearance.weight         # 体重
        self.investigator.personal_data.hair_color = self.appearance.hair_color # 髪の色
        self.investigator.personal_data.eye_color = self.appearance.eye_color   # 瞳の色
        self.investigator.personal_data.skin_color = self.appearance.skin_color # 肌の色

        # Tag
        self.investigator.tag += f"{self.bloodtype.get_name()} {self.personality.get_key()} {self.appearance.body_type_tag} {self.appearance.appearance_rarity}"

        # for test
        buffer = []
        buffer.append(f"性格　: {self.bloodtype.get_description()}で、{self.personality.get_description()}")
        buffer.append(f"学歴　: {self.appearance.final_education}")
        buffer.append(f"体型　: {self.appearance.body_type}")
        buffer.append(f"職業スキル構成　: {skill_composition_string}")

        self.investigator.personal_data.backstory = "\n".join(buffer)           # その他メモ

        # TODO:
        # 戦闘・武器・防具
        # 所持品・所持金

        # 最終更新日時
        #created_at セット済み

    def set_age_correction(self, age: int):
        # NOTE: 年齢による能力値修正
        # ここでは、キャラ生成時に指定した年齢とEDUの関係を修正する。
        # 同時に、P41の年齢による増減をここで計算する。
        # ・年齢下限の「EDU+6」からさらに10歳高くなるごとに、EDU+1する。（40歳以上でもプラス）
        # ・40歳以上の場合、10歳高くなるごとに、STR、CON、DEX、APPのいずれかが減衰する。
        # ・年齢下限より指定年齢が低い場合、EDUを指定年齢の最高値へ強制調整。
        # 　また、10歳低くなるごとに、STR、CON、DEX、APPのいづれかが減衰する。

        # 探索者の年齢下限は「EDU+6」
        limit_lower_age = int(self.investigator.EDU) + 6

        # 40歳以上の場合10歳高くなるごとに減衰する：減衰対象の能力の決定
        attenuation_abilitys = ["strength", "constitution", "dexterity", "appearance"]

        # 増減の方向
        direction = 0 # -1:減少 0:無し 1:増加

        # 増減させるべき値（処理結果格納）
        other = {}
        other["strength"] = 0
        other["constitution"] = 0
        other["dexterity"] = 0
        other["appearance"] = 0
        other["education"] = 0

        if age < limit_lower_age:
            # 減衰
            # 指定した年齢が下限より小さい場合はマイナス補正する。（ルルブには無い独自補正）
            # 10歳低くなるごとに減衰する：減衰対象の選択は40歳以上の時と同様とする。
            direction = -1
            # 修正回数
            correction_count = math.floor((limit_lower_age - age) / 10)

            # EDU調整
            # 例）age = 13  ※最低年齢12歳として、11歳指定はエラーとする。
            # 13歳の最高EDUは「7」(age:13 - 6)
            # ダイス出目が19とすると、EDU=19 + 6 = 25歳が最低年齢
            # この場合EDUは適正の7であるべきなので、差は-12となる。
            other["education"] = (age - 6) - int(self.investigator.EDU)

            # 修正回数が１回以上あるなら調整あり。
            for count in range(0, correction_count):
                # 調整対象能力値の選択
                attenuation_ability = random.choice(attenuation_abilitys)
                other[attenuation_ability] += direction

        elif age < 40:
            # 年齢が40未満の場合は増加方向とする。（ルルブ記載補正）
            direction = 1
            # 修正回数
            correction_count = math.floor((age - limit_lower_age) / 10)

            # EDU調整（10歳超えた回数分プラスする）
            other["education"] = correction_count

            # このケースでは、STR、CON、DEX、APPの増減なし
        else:
            # 年齢が40以上の場合は減衰方向とする。（ルルブ記載補正）
            direction = -1
            # 修正回数
            correction_count = math.floor((age - limit_lower_age) / 10)
            # EDU調整（10歳超えた回数分プラスする）
            other["education"] = correction_count

            # 修正回数が１回以上あるなら調整あり。
            for count in range(0, correction_count):
                # 40歳を超えてから減衰する。
                #print(limit_lower_age + ((count + 1) * 10))
                if (limit_lower_age + ((count + 1) * 10)) >= 40:
                    # 調整対象能力値の選択
                    attenuation_ability = random.choice(attenuation_abilitys)
                    other[attenuation_ability] += direction

        self.investigator.characteristics["strength"].other += other["strength"]
        self.investigator.characteristics["constitution"].other += other["constitution"]
        self.investigator.characteristics["dexterity"].other += other["dexterity"]
        self.investigator.characteristics["appearance"].other += other["appearance"]
        self.investigator.characteristics["education"].other += other["education"]

