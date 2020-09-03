#!/usr/bin/env python3
# -*- coding: utf-8 -*-



class Character():
    def __init__(self):
        self.author_id = ""         # 所有者ID
        self.author_name = ""       # 所有者名
        self.unique_key = ""        # Key
        self.active = ""            # Active
        self.name = ""              # 名前
        self.site_url = ""          # SiteUrl

        # パーソナルデータ
        self.tag = ""               # タグ
        self.occupation = ""        # 職業
        self.age = ""               # 年齢
        self.sex = ""               # 性別
        self.height = ""            # 身長
        self.weight = ""            # 体重
        self.birthplace = ""        # 出身地
        self.residence = ""         # 居住地
        self.hair_color = ""        # 髪の色
        self.eye_color = ""         # 瞳の色
        self.skin_color = ""        # 肌の色

        # 能力値
        self.base_str = 0
        self.base_con = 0
        self.base_pow = 0
        self.base_dex = 0
        self.base_app = 0
        self.base_siz = 0
        self.base_int = 0
        self.base_edu = 0
        self.base_hp = 0
        self.base_mp = 0
        self.base_san = 0
        self.base_idea = 0
        self.base_luck = 0
        self.base_knowledge = 0

        # その他増加分
        self.other_str = 0
        self.other_con = 0
        self.other_pow = 0
        self.other_dex = 0
        self.other_app = 0
        self.other_siz = 0
        self.other_int = 0
        self.other_edu = 0
        self.other_hp = 0
        self.other_mp = 0
        self.other_san = 0
        self.other_idea = 0
        self.other_luck = 0
        self.other_knowledge = 0

        # 一時的増減
        self.temp_str = 0
        self.temp_con = 0
        self.temp_pow = 0
        self.temp_dex = 0
        self.temp_app = 0
        self.temp_siz = 0
        self.temp_int = 0
        self.temp_edu = 0
        self.temp_hp = 0
        self.temp_mp = 0
        self.temp_san = 0
        self.temp_idea = 0
        self.temp_luck = 0
        self.temp_knowledge = 0

        # 現在値
        self.current_str = 0
        self.current_con = 0
        self.current_pow = 0
        self.current_dex = 0
        self.current_app = 0
        self.current_siz = 0
        self.current_int = 0
        self.current_edu = 0
        self.current_hp = 0
        self.current_mp = 0
        self.current_san = 0
        self.current_idea = 0
        self.current_luck = 0
        self.current_knowledge = 0

        # SAN値
        self.current_san = 0
        self.max_san = 0
        self.undefined_area_san = 0

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
        self.memo = ""

