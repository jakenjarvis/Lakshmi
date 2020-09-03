#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json

from contents.AbstractCharacterGetter import AbstractCharacterGetter
from contents.Character import Character

class CharacterVampireBloodNetGetter(AbstractCharacterGetter):
    def __init__(self):
        pass

    def request(self, site_url: str) -> Character:
        result = None
        # https://charasheet.vampire-blood.net/help/webif
        request_url = site_url + ".js"

        response = None
        data = None
        try:
            response = requests.get(request_url)
            data = response.json()
        except Exception as e:
            response = None

        if response:
            result = Character()

            result.author_id = ""                   # 所有者ID
            result.author_name = ""                 # 所有者名
            result.unique_key = ""                  # Key
            result.active = ""                      # Active
            result.name = data["pc_name"]           # 名前
            result.site_url = site_url              # SiteUrl

            # パーソナルデータ
            result.tag = data["pc_tags"]            # タグ
            result.occupation = data["shuzoku"]     # 職業
            result.age = data["age"]                # 年齢
            result.sex = data["sex"]                # 性別
            result.height = data["pc_height"]       # 身長
            result.weight = data["pc_weight"]       # 体重
            result.birthplace = data["pc_kigen"]    # 出身地
            result.residence = ""                   # 居住地
            result.hair_color = data["color_hair"]  # 髪の色
            result.eye_color = data["color_eye"]    # 瞳の色
            result.skin_color = data["color_skin"]  # 肌の色

            # 能力値
            result.base_str = data["NA1"]
            result.base_con = data["NA2"]
            result.base_pow = data["NA3"]
            result.base_dex = data["NA4"]
            result.base_app = data["NA5"]
            result.base_siz = data["NA6"]
            result.base_int = data["NA7"]
            result.base_edu = data["NA8"]
            result.base_hp = data["NA9"]
            result.base_mp = data["NA10"]
            result.base_san = data["NA11"]
            result.base_idea = data["NA12"]
            result.base_luck = data["NA13"]
            result.base_knowledge = data["NA14"]

            # その他増加分
            result.other_str = data["NS1"]
            result.other_con = data["NS2"]
            result.other_pow = data["NS3"]
            result.other_dex = data["NS4"]
            result.other_app = data["NS5"]
            result.other_siz = data["NS6"]
            result.other_int = data["NS7"]
            result.other_edu = data["NS8"]
            result.other_hp = data["NS9"]
            result.other_mp = data["NS10"]
            result.other_san = data["NS11"]
            result.other_idea = data["NS12"]
            result.other_luck = data["NS13"]
            result.other_knowledge = data["NS14"]

            # 一時的増減
            result.temp_str = data["NM1"]
            result.temp_con = data["NM2"]
            result.temp_pow = data["NM3"]
            result.temp_dex = data["NM4"]
            result.temp_app = data["NM5"]
            result.temp_siz = data["NM6"]
            result.temp_int = data["NM7"]
            result.temp_edu = data["NM8"]
            result.temp_hp = data["NM9"]
            result.temp_mp = data["NM10"]
            result.temp_san = data["NM11"]
            result.temp_idea = data["NM12"]
            result.temp_luck = data["NM13"]
            result.temp_knowledge = data["NM14"]

            # 現在値
            result.current_str = data["NP1"]
            result.current_con = data["NP2"]
            result.current_pow = data["NP3"]
            result.current_dex = data["NP4"]
            result.current_app = data["NP5"]
            result.current_siz = data["NP6"]
            result.current_int = data["NP7"]
            result.current_edu = data["NP8"]
            result.current_hp = data["NP9"]
            result.current_mp = data["NP10"]
            result.current_san = data["NP11"]
            result.current_idea = data["NP12"]
            result.current_luck = data["NP13"]
            result.current_knowledge = data["NP14"]

            # SAN値
            result.current_san = data["SAN_Left"]
            result.max_san = data["SAN_Max"]
            result.undefined_area_san = data["SAN_Danger"]

            # TODO:
            # 技能
            # 戦闘技能
            # 探索技能
            # 行動技能
            # 交渉技能
            # 知識技能
            # 戦闘・武器・防具
            # 所持品・所持金

            # その他メモ
            result.memo = data["pc_making_memo"]

        return result

    def get(self, unique_key: str) -> Character:
        pass

    def register(self, character: Character):
        pass
