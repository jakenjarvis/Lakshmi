#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict
from dataclasses import dataclass, fields, field

import math
import datetime
import pytz

# パーソナルデータ
@dataclass
class PersonalData:
    name: str = ""              # 名前
    occupation: str = ""        # 職業
    age: str = ""               # 年齢
    sex: str = ""               # 性別
    residence: str = ""         # 居住地
    birthplace: str = ""        # 出身地

    height: str = ""            # 身長
    weight: str = ""            # 体重
    hair_color: str = ""        # 髪の色
    eye_color: str = ""         # 瞳の色
    skin_color: str = ""        # 肌の色

    backstory: str = ""         # その他メモ

# SAN値
@dataclass
class SanityPoints:
    current: int = 0            # 現在SAN値
    max_insane: int = 0         # 最大SAN値
    indef_insane:int = 0        # 不定の狂気(indefinite insane)

# 能力セット
@dataclass
class AbilitySet:
    ability_name: str           # アビリティ名

    base: int = 0               # 基礎能力値
    other: int = 0              # その他増加分
    temp: int = 0               # 一時的増減
    current: int = 0            # 現在値

    def __hash__(self):
        return hash(self.ability_name)

    def set_values(self, base, other, temp, current):
        self.base = base
        self.other = other
        self.temp = temp
        self.current = current
        return self

    def set_initial_value(self, initial: int):
        self.base = int(initial)
        self.other = 0
        self.temp = 0
        self.current = int(initial)
        return self

    def get_fullname(self):
        return f"{self.ability_name}"

    def to_display_string(self):
        return f"{self.ability_name}: {self.current}"

    def to_full_display_string(self):
        return f"{self.get_fullname()}: ({self.base}+{self.other}+{self.temp})= {self.current}"

    def calculate(self):
        self.current = int(self.base) + int(self.other) + int(self.temp)

# 技能セット
@dataclass
class SkillSet():
    skill_name: str             # スキル名
    skill_subname: str          # サブスキル名

    skill_type: str = "default" # default:標準スキル, additions:追加スキル

    growth_check: bool = False  # 成長チェック
    base: int = 0               # 初期値(基礎値)
    occupation: int = 0         # 職業ポイント
    interest: int = 0           # 興味ポイント
    growth: int = 0             # 成長分
    other: int = 0              # その他増加分
    current: int = 0            # 現在値

    def __hash__(self):
        return hash(f"{self.skill_type}-{self.skill_name}-{self.skill_subname}")

    def set_values(self, growth_check, base, occupation, interest, growth, other, current):
        self.growth_check = bool(growth_check)
        self.base = base
        self.occupation = occupation
        self.interest = interest
        self.growth = growth
        self.other = other
        self.current = current
        return self

    def set_initial_value(self, initial: int):
        self.growth_check = False
        self.base = int(initial)
        self.occupation = 0
        self.interest = 0
        self.growth = 0
        self.other = 0
        self.current = int(initial)
        return self

    def get_fullname(self):
        result = ""
        if len(self.skill_subname.strip()) >= 1:
            result = f"{self.skill_name}({self.skill_subname})"
        else:
            result = f"{self.skill_name}"
        return result

    def to_display_string(self):
        return f"{self.get_fullname()}: {self.current}"

    def to_full_display_string(self):
        return f"{self.get_fullname()}: ({self.base}+{self.occupation}+{self.interest}+{self.growth}+{self.other})= {self.current}"

    def calculate(self):
        self.current = int(self.base) + int(self.occupation) + int(self.interest) + int(self.growth) + int(self.other)

# 技能ポイント
@dataclass
class SkillPoints:
    remaining_occupation: int = 0   # 残り職業ポイント
    remaining_interest: int = 0     # 残り興味ポイント
    max_occupation: int = 0         # 最大職業ポイント
    max_interest: int = 0           # 最大興味ポイント
    additions_occupation: int = 0   # 追加職業ポイント
    additions_interest: int = 0     # 追加興味ポイント

# スキルの初期値
class InitialValueOfSkills():
    def __init__(self, dex: int, edu: int):
        self.values = {
            # 戦闘技能
            "dodge" : dex * 2,          # 回避
            "kick" : 25,                # キック
            "grapple" : 25,             # 組み付き
            "fist_punch" : 50,          # こぶし(パンチ)
            "head_butt" : 10,           # 頭突き
            "throw" : 25,               # 投擲
            "martial_arts" : 1,         # マーシャルアーツ
            "handgun" : 20,             # 拳銃
            "smg" : 15,                 # サブマシンガン
            "shotgun" : 30,             # ショットガン
            "machine_gun" : 15,         # マシンガン
            "rifle" : 25,               # ライフル

            # 探索技能
            "first_aid" : 30,           # 応急手当
            "locksmith" : 1,            # 鍵開け
            "conceal" : 15,             # 隠す
            "hide" : 10,                # 隠れる
            "listen" : 25,              # 聞き耳
            "sneak" : 10,               # 忍び歩き
            "photography" : 10,         # 写真術
            "psychoanalysis" : 1,       # 精神分析
            "track" : 10,               # 追跡
            "climb" : 40,               # 登攀
            "library_use" : 25,         # 図書館
            "spot_hidden" : 25,         # 目星

            # 行動技能
            "drive" : 20,               # 運転
            "mech_repair" : 20,         # 機械修理
            "opr_hvy_machine" : 1,      # 重機械操作
            "ride" : 5,                 # 乗馬
            "swim" : 25,                # 水泳
            "craft" : 5,                # 製作
            "pilot" : 1,                # 操縦
            "jump" : 25,                # 跳躍
            "electr_repair" : 10,       # 電気修理
            "navigate" : 10,            # ナビゲート
            "disguise" : 1,             # 変装

            # 交渉技能
            "fast_talk" : 5,            # 言いくるめ
            "credit_rating" : 15,       # 信用
            "persuade" : 15,            # 説得
            "bargain" : 5,              # 値切り
            "own_language" : edu * 5,   # 母国語
            #"other_language" : 1,       # その他の言語(注)

            # 知識技能
            "medicine" : 5,             # 医学
            "occult" : 5,               # オカルト
            "chemistry" : 1,            # 化学
            "cthulhu_mythos" : 0,       # クトゥルフ神話
            "art" : 5,                  # 芸術
            "accounting" : 10,          # 経理
            "archeology" : 1,           # 考古学
            "computer" : 1,             # コンピューター
            "psychology" : 5,           # 心理学
            "anthropology" : 1,         # 人類学
            "biology" : 1,              # 生物学
            "geology" : 1,              # 地質学
            "electronics" : 1,          # 電子工学
            "astronomy" : 1,            # 天文学
            "natural_history" : 10,     # 博物学
            "physics" : 1,              # 物理学
            "law" : 5,                  # 法律
            "pharmacy" : 1,             # 薬学
            "history" : 20,             # 歴史
        }

    def get_value(self, key: str) -> int:
        return int(self.values[key] if key in self.values else 1)

# 探索者
@dataclass
class Investigator:
    unique_id: str = ""        # Key
    site_id1: str = ""          # SiteId1
    site_id2: str = ""          # SiteId2
    site_url: str = ""          # SiteUrl
    site_name: str = ""         # SiteName
    site_favicon_url: str = ""  # SiteFaviconUrl
    author_id: str = ""         # 所有者ID
    author_name: str = ""       # 所有者名
    active: bool = False        # Active
    lost: bool = False          # Lost
    tag: str = ""               # タグ
    image_url: str = ""         # 画像URL

    # 特徴
    characteristics: Dict[str, AbilitySet] = field(default_factory=lambda: {
        "strength"              : AbilitySet("STR"),
        "constitution"          : AbilitySet("CON"),
        "power"                 : AbilitySet("POW"),
        "dexterity"             : AbilitySet("DEX"),
        "appearance"            : AbilitySet("APP"),
        "size"                  : AbilitySet("SIZ"),
        "intelligence"          : AbilitySet("INT"),
        "education"             : AbilitySet("EDU"),
        "hit_points"            : AbilitySet("HP"),
        "magic_points"          : AbilitySet("MP"),
        "initial_sanity"        : AbilitySet("初期SAN"),
        "idea"                  : AbilitySet("アイデア"),
        "luck"                  : AbilitySet("幸運"),
        "knowledge"             : AbilitySet("知識"),
    })

    # SAN値
    sanity_points: SanityPoints = field(default_factory=SanityPoints)
    # 技能
    skill_points: SkillPoints = field(default_factory=SkillPoints)

    # 戦闘技能
    combat_skills: Dict[str, SkillSet] = field(default_factory=lambda: {
        "dodge"                 : SkillSet("回避", ""),
        "kick"                  : SkillSet("キック", ""),
        "grapple"               : SkillSet("組み付き", ""),
        "fist_punch"            : SkillSet("こぶし", "パンチ"),
        "head_butt"             : SkillSet("頭突き", ""),
        "throw"                 : SkillSet("投擲", ""),
        "martial_arts"          : SkillSet("マーシャルアーツ", ""),
        "handgun"               : SkillSet("拳銃", ""),
        "smg"                   : SkillSet("サブマシンガン", ""),
        "shotgun"               : SkillSet("ショットガン", ""),
        "machine_gun"           : SkillSet("マシンガン", ""),
        "rifle"                 : SkillSet("ライフル", ""),
    })
    # 探索技能
    search_skills: Dict[str, SkillSet] = field(default_factory=lambda: {
        "first_aid"             : SkillSet("応急手当", ""),
        "locksmith"             : SkillSet("鍵開け", ""),
        "conceal"               : SkillSet("隠す", ""),
        "hide"                  : SkillSet("隠れる", ""),
        "listen"                : SkillSet("聞き耳", ""),
        "sneak"                 : SkillSet("忍び歩き", ""),
        "photography"           : SkillSet("写真術", ""),
        "psychoanalysis"        : SkillSet("精神分析", ""),
        "track"                 : SkillSet("追跡", ""),
        "climb"                 : SkillSet("登攀", ""),
        "library_use"           : SkillSet("図書館", ""),
        "spot_hidden"           : SkillSet("目星", ""),
    })
    # 行動技能
    behavioral_skills: Dict[str, SkillSet] = field(default_factory=lambda: {
        "drive"                 : SkillSet("運転", ""),
        "mech_repair"           : SkillSet("機械修理", ""),
        "opr_hvy_machine"       : SkillSet("重機械操作", ""),
        "ride"                  : SkillSet("乗馬", ""),
        "swim"                  : SkillSet("水泳", ""),
        "craft"                 : SkillSet("製作", ""),
        "pilot"                 : SkillSet("操縦", ""),
        "jump"                  : SkillSet("跳躍", ""),
        "electr_repair"         : SkillSet("電気修理", ""),
        "navigate"              : SkillSet("ナビゲート", ""),
        "disguise"              : SkillSet("変装", ""),
    })
    # 交渉技能
    negotiation_skills: Dict[str, SkillSet] = field(default_factory=lambda: {
        "fast_talk"             : SkillSet("言いくるめ", ""),
        "credit_rating"         : SkillSet("信用", ""),
        "persuade"              : SkillSet("説得", ""),
        "bargain"               : SkillSet("値切り", ""),
        "own_language"          : SkillSet("母国語", ""),
    })
    # 知識技能
    knowledge_skills: Dict[str, SkillSet] = field(default_factory=lambda: {
        "medicine"              : SkillSet("医学", ""),
        "occult"                : SkillSet("オカルト", ""),
        "chemistry"             : SkillSet("化学", ""),
        "cthulhu_mythos"        : SkillSet("クトゥルフ神話", ""),
        "art"                   : SkillSet("芸術", ""),
        "accounting"            : SkillSet("経理", ""),
        "archeology"            : SkillSet("考古学", ""),
        "computer"              : SkillSet("コンピューター", ""),
        "psychology"            : SkillSet("心理学", ""),
        "anthropology"          : SkillSet("人類学", ""),
        "biology"               : SkillSet("生物学", ""),
        "geology"               : SkillSet("地質学", ""),
        "electronics"           : SkillSet("電子工学", ""),
        "astronomy"             : SkillSet("天文学", ""),
        "natural_history"       : SkillSet("博物学", ""),
        "physics"               : SkillSet("物理学", ""),
        "law"                   : SkillSet("法律", ""),
        "pharmacy"              : SkillSet("薬学", ""),
        "history"               : SkillSet("歴史", ""),
    })

    # 戦闘・武器・防具
    # TODO:
    # 所持品・所持金
    # TODO:

    # TODO: P40 ダメージボーナス

    # パーソナルデータ
    personal_data: PersonalData = field(default_factory=PersonalData)
    # 最終更新日時
    created_at: datetime = field(default_factory=lambda: datetime.datetime.now(pytz.timezone('Asia/Tokyo')), init=False)


    # 名前
    @property
    def character_name(self):
        return self.personal_data.name

    # 画像URL
    @property
    def character_image_url(self):
        return self.image_url

    # 職業
    @property
    def occupation(self):
        return self.personal_data.occupation

    # 年齢
    @property
    def age(self):
        return self.personal_data.age

    # 性別
    @property
    def sex(self):
        return self.personal_data.sex

    # その他メモ
    @property
    def backstory(self):
        return self.personal_data.backstory


    @property
    def STR(self):
        return self.characteristics["strength"].current
    @property
    def CON(self):
        return self.characteristics["constitution"].current
    @property
    def POW(self):
        return self.characteristics["power"].current
    @property
    def DEX(self):
        return self.characteristics["dexterity"].current
    @property
    def APP(self):
        return self.characteristics["appearance"].current
    @property
    def SIZ(self):
        return self.characteristics["size"].current
    @property
    def INT(self):
        return self.characteristics["intelligence"].current
    @property
    def EDU(self):
        return self.characteristics["education"].current
    @property
    def HP(self):
        return self.characteristics["hit_points"].current
    @property
    def MP(self):
        return self.characteristics["magic_points"].current
    @property
    def SAN(self):
        return self.characteristics["initial_sanity"].current
    @property
    def IDEA(self):
        return self.characteristics["idea"].current
    @property
    def LUCK(self):
        return self.characteristics["luck"].current
    @property
    def KNOWLEDGE(self):
        return self.characteristics["knowledge"].current

    def calculate(self):
        # 現在能力値の再計算
        for key in self.characteristics.keys():
            abilityset = self.characteristics[key]
            abilityset.calculate()

        # 能力値初期値の再計算
        self.characteristics["hit_points"].set_initial_value(math.ceil((self.CON + self.SIZ) / 2))
        self.characteristics["magic_points"].set_initial_value(self.POW * 1)
        self.characteristics["initial_sanity"].set_initial_value(self.POW * 5)
        self.characteristics["idea"].set_initial_value(self.INT * 5)
        self.characteristics["luck"].set_initial_value(self.POW * 5)
        self.characteristics["knowledge"].set_initial_value(self.EDU * 5)

        # 現在能力値の再計算
        for key in self.characteristics.keys():
            abilityset = self.characteristics[key]
            abilityset.calculate()

        # スキル初期値作成
        initializer = InitialValueOfSkills(self.DEX, self.EDU)

        # 現在スキル値の初期値設定と再計算
        skills = [self.combat_skills, self.search_skills, self.behavioral_skills, self.negotiation_skills, self.knowledge_skills]
        for skill in skills:
            for key in skill.keys():
                skillset = skill[key]
                skillset.base = initializer.get_value(key)
                skillset.calculate()

        # SAN値
        self.sanity_points.max_insane = 99 - int(self.knowledge_skills["cthulhu_mythos"].current)
        self.sanity_points.indef_insane = int(self.sanity_points.max_insane) - int(self.sanity_points.current)

        # スキルポイントの合算
        sum_skill_occupation = 0    # 職業P合計
        sum_skill_interest = 0      # 趣味P合計
        for skill in skills:
            for key in skill.keys():
                skillset = skill[key]
                # 職業P合計
                sum_skill_occupation += skillset.occupation
                # 趣味P合計
                sum_skill_interest += skillset.interest

        # 技能
        # 最大職業ポイント
        self.skill_points.max_occupation = (self.EDU * 20) + self.skill_points.additions_occupation
        # 最大興味ポイント
        self.skill_points.max_interest = (self.INT * 10) + self.skill_points.additions_interest

        # 残り職業ポイント
        self.skill_points.remaining_occupation = self.skill_points.max_occupation - sum_skill_occupation
        # 残り興味ポイント
        self.skill_points.remaining_interest = self.skill_points.max_interest - sum_skill_interest

        return self
