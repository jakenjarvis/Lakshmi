#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict
import math
import random

class CharacterBloodType():
    def __init__(self):
        # 血液型タイプ
        # 全スキル別の「重み付け」に影響を与えるものとする。
        self.blood_types = {
            # 思考タイプ
            "A" : {
                "name": "A型",
                "description": "物事を論理的に捉えて理屈で判断するタイプ",
                "priority": [
                    "computer",             # コンピューター
                    "electronics",          # 電子工学
                    "medicine",             # 医学
                    "pharmacy",             # 薬学
                    "accounting",           # 経理
                    "chemistry",            # 化学
                    "law",                  # 法律
                    "psychology",           # 心理学
                    "library_use",          # 図書館
                    "listen",               # 聞き耳
                    "spot_hidden",          # 目星
                    "first_aid",            # 応急手当
                    "psychoanalysis",       # 精神分析
                    "locksmith",            # 鍵開け
                    "conceal",              # 隠す
                    "hide",                 # 隠れる
                    "sneak",                # 忍び歩き
                    "dodge",                # 回避
                    "fast_talk",            # 言いくるめ
                    "credit_rating",        # 信用
                    "persuade",             # 説得
                    "bargain",              # 値切り
                    "own_language",         # 母国語
                    "other_language",       # その他の言語(注)
                    "occult",               # オカルト
                    "art",                  # 芸術
                    "photography",          # 写真術
                    "mech_repair",          # 機械修理
                    "electr_repair",        # 電気修理
                    "opr_hvy_machine",      # 重機械操作
                    "craft",                # 製作
                    "swim",                 # 水泳
                    "jump",                 # 跳躍
                    "disguise",             # 変装
                    "track",                # 追跡
                    "climb",                # 登攀
                    "throw",                # 投擲
                    "handgun",              # 拳銃
                    "smg",                  # サブマシンガン
                    "shotgun",              # ショットガン
                    "machine_gun",          # マシンガン
                    "rifle",                # ライフル
                    "martial_arts",         # マーシャルアーツ
                    "kick",                 # キック
                    "grapple",              # 組み付き
                    "head_butt",            # 頭突き
                    "fist_punch",           # こぶし(パンチ)
                    "anthropology",         # 人類学
                    "biology",              # 生物学
                    "geology",              # 地質学
                    "astronomy",            # 天文学
                    "natural_history",      # 博物学
                    "physics",              # 物理学
                    "archeology",           # 考古学
                    "history",              # 歴史
                    "navigate",             # ナビゲート
                    "pilot",                # 操縦
                    "drive",                # 運転
                    "ride",                 # 乗馬
                ],
            },
            # 感覚タイプ
            "B" : {
                "name": "B型",
                "description": "物事を理屈抜きに捉えるタイプ",
                "priority": [
                    "dodge",                # 回避
                    "fast_talk",            # 言いくるめ
                    "credit_rating",        # 信用
                    "persuade",             # 説得
                    "bargain",              # 値切り
                    "listen",               # 聞き耳
                    "spot_hidden",          # 目星
                    "first_aid",            # 応急手当
                    "psychoanalysis",       # 精神分析
                    "martial_arts",         # マーシャルアーツ
                    "kick",                 # キック
                    "grapple",              # 組み付き
                    "head_butt",            # 頭突き
                    "fist_punch",           # こぶし(パンチ)
                    "locksmith",            # 鍵開け
                    "conceal",              # 隠す
                    "hide",                 # 隠れる
                    "sneak",                # 忍び歩き
                    "swim",                 # 水泳
                    "jump",                 # 跳躍
                    "disguise",             # 変装
                    "track",                # 追跡
                    "climb",                # 登攀
                    "throw",                # 投擲
                    "navigate",             # ナビゲート
                    "pilot",                # 操縦
                    "drive",                # 運転
                    "ride",                 # 乗馬
                    "own_language",         # 母国語
                    "other_language",       # その他の言語(注)
                    "psychology",           # 心理学
                    "library_use",          # 図書館
                    "anthropology",         # 人類学
                    "biology",              # 生物学
                    "geology",              # 地質学
                    "astronomy",            # 天文学
                    "natural_history",      # 博物学
                    "physics",              # 物理学
                    "archeology",           # 考古学
                    "history",              # 歴史
                    "computer",             # コンピューター
                    "electronics",          # 電子工学
                    "medicine",             # 医学
                    "pharmacy",             # 薬学
                    "accounting",           # 経理
                    "chemistry",            # 化学
                    "law",                  # 法律
                    "mech_repair",          # 機械修理
                    "electr_repair",        # 電気修理
                    "opr_hvy_machine",      # 重機械操作
                    "handgun",              # 拳銃
                    "smg",                  # サブマシンガン
                    "shotgun",              # ショットガン
                    "machine_gun",          # マシンガン
                    "rifle",                # ライフル
                    "craft",                # 製作
                    "art",                  # 芸術
                    "photography",          # 写真術
                    "occult",               # オカルト
                ],
            },
            # 感情タイプ
            "O" : {
                "name": "O型",
                "description": "自分の好き嫌いや喜怒哀楽を重視するタイプ",
                "priority": [
                    "fast_talk",            # 言いくるめ
                    "credit_rating",        # 信用
                    "persuade",             # 説得
                    "bargain",              # 値切り
                    "own_language",         # 母国語
                    "other_language",       # その他の言語(注)
                    "locksmith",            # 鍵開け
                    "dodge",                # 回避
                    "library_use",          # 図書館
                    "listen",               # 聞き耳
                    "spot_hidden",          # 目星
                    "first_aid",            # 応急手当
                    "conceal",              # 隠す
                    "hide",                 # 隠れる
                    "sneak",                # 忍び歩き
                    "handgun",              # 拳銃
                    "smg",                  # サブマシンガン
                    "shotgun",              # ショットガン
                    "machine_gun",          # マシンガン
                    "rifle",                # ライフル
                    "navigate",             # ナビゲート
                    "pilot",                # 操縦
                    "drive",                # 運転
                    "ride",                 # 乗馬
                    "occult",               # オカルト
                    "art",                  # 芸術
                    "photography",          # 写真術
                    "mech_repair",          # 機械修理
                    "electr_repair",        # 電気修理
                    "opr_hvy_machine",      # 重機械操作
                    "craft",                # 製作
                    "swim",                 # 水泳
                    "jump",                 # 跳躍
                    "disguise",             # 変装
                    "track",                # 追跡
                    "climb",                # 登攀
                    "throw",                # 投擲
                    "anthropology",         # 人類学
                    "biology",              # 生物学
                    "geology",              # 地質学
                    "astronomy",            # 天文学
                    "natural_history",      # 博物学
                    "physics",              # 物理学
                    "archeology",           # 考古学
                    "history",              # 歴史
                    "psychoanalysis",       # 精神分析
                    "psychology",           # 心理学
                    "computer",             # コンピューター
                    "electronics",          # 電子工学
                    "medicine",             # 医学
                    "pharmacy",             # 薬学
                    "accounting",           # 経理
                    "chemistry",            # 化学
                    "law",                  # 法律
                    "martial_arts",         # マーシャルアーツ
                    "kick",                 # キック
                    "grapple",              # 組み付き
                    "head_butt",            # 頭突き
                    "fist_punch",           # こぶし(パンチ)
                ],
            },
            # 直観タイプ
            "AB" : {
                "name": "AB型",
                "description": "物事の本質を閃きで捉えるタイプ",
                "priority": [
                    "art",                  # 芸術
                    "photography",          # 写真術
                    "occult",               # オカルト
                    "navigate",             # ナビゲート
                    "pilot",                # 操縦
                    "drive",                # 運転
                    "ride",                 # 乗馬
                    "psychology",           # 心理学
                    "library_use",          # 図書館
                    "listen",               # 聞き耳
                    "spot_hidden",          # 目星
                    "first_aid",            # 応急手当
                    "psychoanalysis",       # 精神分析
                    "craft",                # 製作
                    "swim",                 # 水泳
                    "jump",                 # 跳躍
                    "disguise",             # 変装
                    "track",                # 追跡
                    "climb",                # 登攀
                    "throw",                # 投擲
                    "conceal",              # 隠す
                    "hide",                 # 隠れる
                    "sneak",                # 忍び歩き
                    "dodge",                # 回避
                    "locksmith",            # 鍵開け
                    "anthropology",         # 人類学
                    "biology",              # 生物学
                    "geology",              # 地質学
                    "astronomy",            # 天文学
                    "natural_history",      # 博物学
                    "physics",              # 物理学
                    "archeology",           # 考古学
                    "history",              # 歴史
                    "martial_arts",         # マーシャルアーツ
                    "kick",                 # キック
                    "grapple",              # 組み付き
                    "head_butt",            # 頭突き
                    "fist_punch",           # こぶし(パンチ)
                    "medicine",             # 医学
                    "pharmacy",             # 薬学
                    "accounting",           # 経理
                    "chemistry",            # 化学
                    "law",                  # 法律
                    "fast_talk",            # 言いくるめ
                    "credit_rating",        # 信用
                    "persuade",             # 説得
                    "bargain",              # 値切り
                    "own_language",         # 母国語
                    "other_language",       # その他の言語(注)
                    "computer",             # コンピューター
                    "electronics",          # 電子工学
                    "mech_repair",          # 機械修理
                    "electr_repair",        # 電気修理
                    "opr_hvy_machine",      # 重機械操作
                    "handgun",              # 拳銃
                    "smg",                  # サブマシンガン
                    "shotgun",              # ショットガン
                    "machine_gun",          # マシンガン
                    "rifle",                # ライフル
                ],
            },
        }

        self.bloodtype_key = self.choice_blood_type()

    def choice_blood_type(self) -> str:
        # 血液型リストから公平に選択する。
        return random.choice(list(self.blood_types.keys()))

    def get_key(self) -> str:
        return self.bloodtype_key

    def get_name(self) -> str:
        return self.blood_types[self.bloodtype_key]["name"]

    def get_description(self) -> str:
        return self.blood_types[self.bloodtype_key]["description"]

    def get_skills_priority(self) -> List[str]:
        return self.blood_types[self.bloodtype_key]["priority"]
