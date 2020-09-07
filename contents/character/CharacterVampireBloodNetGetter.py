#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import re

import LakshmiErrors
from contents.character.Investigator import Investigator, SkillSet
from contents.character.AbstractCharacterGetter import AbstractCharacterGetter

class CharacterVampireBloodNetGetter(AbstractCharacterGetter):
    DETECT_TARGET_URL = re.compile(r"^.*charasheet\.vampire\-blood\.net.*$", re.IGNORECASE)
    SKILL_TITLE_SPLIT = re.compile(r"^([^（【〔［《『「(\[）】〕］》』」)\]]+)([（【〔［《『「(\[]+)([^）】〕］》』」)\]]+)([）】〕］》』」)\]])?$", re.IGNORECASE)

    def __init__(self):
        pass

    @classmethod
    def get_site_title(self) -> str:
        return "キャラクター保管所 (charasheet.vampire-blood.net)"

    @classmethod
    def is_detect_url(self, site_url: str) -> bool:
        return (CharacterVampireBloodNetGetter.DETECT_TARGET_URL.search(site_url) != None)

    @classmethod
    def get_favicon_url(self) -> str:
        return "https://www.google.com/s2/favicons?domain=charasheet.vampire-blood.net"

    @classmethod
    def request(self, instance: Investigator, site_url: str) -> bool:
        result = False
        response = None
        data = None
        try:
            # https://charasheet.vampire-blood.net/help/webif
            request_url = site_url + ".js"
            response = requests.get(request_url)
            data = response.json()
        except Exception as e:
            response = None

        # COCのデータでなければ拒否する。
        if data["game"] != "coc":
            raise LakshmiErrors.NotCallOfCthulhuInvestigatorException()

        if response:
            # NOTE: 基本的に上書きできない項目は触らないこと。
            #instance.unique_id = ""                              # Key
            instance.site_id1 = str(data["data_id"])                # SiteId1
            instance.site_id2 = str(data["phrase"])                 # SiteId2
            instance.site_url = site_url                            # SiteUrl
            instance.site_name = self.get_site_title()              # SiteName
            instance.site_favicon_url = self.get_favicon_url()      # SiteFaviconUrl
            #instance.author_id = ""                               # 所有者ID
            #instance.author_name = ""                             # 所有者名
            #instance.active = False                               # Active
            instance.tag = data["pc_tags"]                          # タグ
            #instance.image_url = ""                               # 画像URL

            # パーソナルデータ
            instance.personal_data.name = data["pc_name"]             # 名前
            instance.personal_data.occupation = data["shuzoku"]       # 職業
            instance.personal_data.age = data["age"]                  # 年齢
            instance.personal_data.sex = data["sex"]                  # 性別
            #instance.personal_data.residence = ""                     # 居住地
            instance.personal_data.birthplace = data["pc_kigen"]      # 出身地

            instance.personal_data.height = data["pc_height"]         # 身長
            instance.personal_data.weight = data["pc_weight"]         # 体重
            instance.personal_data.hair_color = data["color_hair"]    # 髪の色
            instance.personal_data.eye_color = data["color_eye"]      # 瞳の色
            instance.personal_data.skin_color = data["color_skin"]    # 肌の色

            instance.personal_data.backstory = data["pc_making_memo"] # その他メモ

            # 能力値
            instance.characteristics["strength"].set_values(data["NA1"], data["NS1"], data["NM1"], data["NP1"])
            instance.characteristics["constitution"].set_values(data["NA2"], data["NS2"], data["NM2"], data["NP2"])
            instance.characteristics["power"].set_values(data["NA3"], data["NS3"], data["NM3"], data["NP3"])
            instance.characteristics["dexterity"].set_values(data["NA4"], data["NS4"], data["NM4"], data["NP4"])
            instance.characteristics["appearance"].set_values(data["NA5"], data["NS5"], data["NM5"], data["NP5"])
            instance.characteristics["size"].set_values(data["NA6"], data["NS6"], data["NM6"], data["NP6"])
            instance.characteristics["intelligence"].set_values(data["NA7"], data["NS7"], data["NM7"], data["NP7"])
            instance.characteristics["education"].set_values(data["NA8"], data["NS8"], data["NM8"], data["NP8"])
            instance.characteristics["hit_points"].set_values(data["NA9"], data["NS9"], data["NM9"], data["NP9"])
            instance.characteristics["magic_points"].set_values(data["NA10"], data["NS10"], data["NM10"], data["NP10"])
            instance.characteristics["initial_sanity"].set_values(data["NA11"], data["NS11"], data["NM11"], data["NP11"])
            instance.characteristics["idea"].set_values(data["NA12"], data["NS12"], data["NM12"], data["NP12"])
            instance.characteristics["luck"].set_values(data["NA13"], data["NS13"], data["NM13"], data["NP13"])
            instance.characteristics["knowledge"].set_values(data["NA14"], data["NS14"], data["NM14"], data["NP14"])

            # SAN値
            instance.sanity_points.current = data["SAN_Left"]
            instance.sanity_points.max_insane = data["SAN_Max"]
            instance.sanity_points.indef_insane = data["SAN_Danger"]

            # 技能
            instance.skill_points.remaining_occupation = data["TS_Total"] # 残り職業ポイント
            instance.skill_points.remaining_interest = data["TK_Total"]   # 残り興味ポイント
            instance.skill_points.max_occupation = data["TS_Maximum"]     # 最大職業ポイント
            instance.skill_points.max_interest = data["TK_Maximum"]       # 最大興味ポイント
            instance.skill_points.additions_occupation = data["TS_Add"]   # 追加職業ポイント
            instance.skill_points.additions_interest = data["TK_Add"]     # 追加興味ポイント

            # 戦闘技能
            keylists = ["dodge", "kick", "grapple", "fist_punch", "head_butt", "throw", "martial_arts", "handgun", "smg", "shotgun", "machine_gun", "rifle"]
            self.set_skills_values(instance.combat_skills, keylists, data, "TBAU", "TBAD", "TBAS", "TBAK", "TBAA", "TBAO", "TBAP", "TBAName")

            # 探索技能
            keylists = ["first_aid", "locksmith", "conceal", "hide", "listen", "sneak", "photography", "psychoanalysis", "track", "climb", "library_use", "spot_hidden"]
            self.set_skills_values(instance.search_skills, keylists, data, "TFAU", "TFAD", "TFAS", "TFAK", "TFAA", "TFAO", "TFAP", "TFAName")

            # 行動技能
            keylists = ["drive", "mech_repair", "opr_hvy_machine", "ride", "swim", "craft", "pilot", "jump", "electr_repair", "navigate", "disguise"]
            self.set_skills_values(instance.behavioral_skills, keylists, data, "TAAU", "TAAD", "TAAS", "TAAK", "TAAA", "TAAO", "TAAP", "TAAName")

            instance.behavioral_skills["drive"].skill_subname = str(data["unten_bunya"]).strip()
            instance.behavioral_skills["craft"].skill_subname = str(data["seisaku_bunya"]).strip()
            instance.behavioral_skills["pilot"].skill_subname = str(data["main_souju_norimono"]).strip()

            # 交渉技能
            keylists = ["fast_talk", "credit_rating", "persuade", "bargain", "own_language"]
            self.set_skills_values(instance.negotiation_skills, keylists, data, "TCAU", "TCAD", "TCAS", "TCAK", "TCAA", "TCAO", "TCAP", "TCAName")

            instance.negotiation_skills["own_language"].skill_subname = str(data["mylang_name"]).strip()

            # 知識技能
            keylists = ["medicine", "occult", "chemistry", "cthulhu_mythos", "art", "accounting", "archeology", "computer", "psychology",
                "anthropology", "biology", "geology", "electronics", "astronomy", "natural_history", "physics", "law", "pharmacy", "history"]
            self.set_skills_values(instance.knowledge_skills, keylists, data, "TKAU", "TKAD", "TKAS", "TKAK", "TKAA", "TKAO", "TKAP", "TKAName")

            instance.knowledge_skills["art"].skill_subname = str(data["geijutu_bunya"]).strip()

            # TODO:
            # 戦闘・武器・防具
            # 所持品・所持金

            result = True
        return result

    @classmethod
    def set_skills_values(self, skills, defaultkeys, data, growth_checke_key, base_key, occupation_key, interest_key, growth_key, other_key, current_key, additions_name_key):
        # 配列数の取得
        skills_count = len(data[growth_checke_key])

        for index in range(skills_count):
            growth_check = (len(str(data[growth_checke_key][index]).strip()) >= 1)

            if index < len(defaultkeys):
                # デフォルトスキル
                key = defaultkeys[index]
            else:
                # 追加分スキル
                key = f'additions_{index}'

                additions_index = index - len(defaultkeys) - 1
                additions_title = str(data[additions_name_key][additions_index]).strip()

                # スキル名
                skill_name = ""
                skill_subname = ""
                match = CharacterVampireBloodNetGetter.SKILL_TITLE_SPLIT.search(additions_title)
                if match:
                    skill_name = str(match.group(1))
                    skill_subname = str(match.group(3))
                else:
                    skill_name = additions_title
                    skill_subname = ""

                skills[key] = SkillSet(skill_name, skill_subname)
                # スキルタイプ
                skills[key].skill_type = "additions"

            skills[key].set_values(
                # 成長チェック
                growth_check,
                # 初期値(基礎値)
                int(data[base_key][index] or 0),
                # 職業ポイント
                int(data[occupation_key][index] or 0),
                # 興味ポイント
                int(data[interest_key][index] or 0),
                # 成長分
                int(data[growth_key][index] or 0),
                # その他増加分
                int(data[other_key][index] or 0),
                # 現在値
                int(data[current_key][index] or 0),
            )
        return self
