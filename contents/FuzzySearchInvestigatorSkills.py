#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from decimal import Decimal
from typing import List, Dict
from dataclasses import dataclass, fields, field
from discord.ext import commands
import mojimoji

import pandas as pd

from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance

from contents.character.Investigator import Investigator

@dataclass
class OneWord():
    keyword: str

    distance: Decimal = field(default_factory=lambda: Decimal("0.0"))

    def calc(self, search_word: str):
        word1_string = mojimoji.han_to_zen(search_word.lower())
        word2_string = mojimoji.han_to_zen(self.keyword.lower())
        self.distance = Decimal("1.0") - Decimal(str(normalized_damerau_levenshtein_distance(word1_string, word2_string)))
        return self

@dataclass
class SimilarKeyword():
    keywords: List[OneWord] = field(default_factory=list)

    def add(self, targets: List[str]):
        for word in targets:
            self.append(word)
        return self

    def append(self, keyword: str):
        if len(keyword) >= 1:
            self.keywords.append(OneWord(keyword))
        return self

    def calc(self, search_word: str):
        for word in self.keywords:
            word.calc(search_word)
        return self

    def max(self) -> Decimal:
        return max([word.distance for word in self.keywords], default=Decimal("0.0"))

@dataclass
class SearchResult():
    link_name: str = ""             # リンク名
    main_name: str = ""             # メイン名
    sub_name: str = ""              # サブ名

    changed_initial_value: int = 0  # 初期値からの変更（変更なし:0 変更あり:1）
    skill_type: int = 0             # スキルのタイプ（default標準スキル: 0, additions追加スキル:1）
    skill_current_value: int = 0    # スキルの現在値

    max_main_distance: Decimal = field(default_factory=lambda: Decimal("0.0"))
    max_sub_distance: Decimal = field(default_factory=lambda: Decimal("0.0"))
    sum_distance: Decimal = field(default_factory=lambda: Decimal("0.0"))

@dataclass
class SearchKeyword():
    main_keyword: SimilarKeyword = field(default_factory=SimilarKeyword)
    sub_keyword: SimilarKeyword = field(default_factory=SimilarKeyword)

    search_results: SearchResult = field(default_factory=SearchResult)

    def set_initialize(self, link_name, main_name, sub_name, changed_initial_value, skill_type, skill_current_value):
        self.search_results.link_name = link_name
        self.search_results.main_name = main_name
        self.search_results.sub_name = sub_name
        self.search_results.changed_initial_value = changed_initial_value
        self.search_results.skill_type = skill_type
        self.search_results.skill_current_value = skill_current_value
        return self

    def search(self, search_main_word: str, search_sub_word: str):
        self.main_keyword.calc(search_main_word)
        self.sub_keyword.calc(search_sub_word)
        self.search_results.max_main_distance = self.main_keyword.max()
        self.search_results.max_sub_distance = self.sub_keyword.max()
        self.search_results.sum_distance = self.search_results.max_main_distance + self.search_results.max_sub_distance
        return self

class FuzzySearchInvestigatorSkills():
    SKILL_TITLE_SPLIT = re.compile(r"^([^（【〔［《『「(\[）】〕］》』」)\]]+)([（【〔［《『「(\[]+)([^）】〕］》』」)\]]+)([）】〕］》』」)\]])?$", re.IGNORECASE)

    def __init__(self, investigator: Investigator):
        self.investigator = investigator
        self.search_keywords: List[SearchKeyword] = []

        self.dictionary: Dict[str, List[str]] = {}
        # TODO:
        self.dictionary["SAN"] = ["SAN", "さん", "サン"]
        self.dictionary["STR"] = ["STR", "すとれんぐす", "ストレングス", "えすてぃーあーる", "エスティーアール", "sterength"]
        self.dictionary["CON"] = ["CON", "こんすてぃてゅーしょん", "コンスティテューション", "こん", "コン", "constitution"]
        self.dictionary["POW"] = ["POW", "ぱわー", "パワー", "ぱう", "パウ", "ぽう", "ポウ", "power"]
        self.dictionary["DEX"] = ["DEX", "でくすてりてぃ", "デクステリティ", "でっくす", "デックス", "dexterity"]
        self.dictionary["APP"] = ["APP", "あぴあらんす", "アピアランス", "えーぴーぴー", "エーピーピー", "appearance"]
        self.dictionary["SIZ"] = ["SIZ", "さいず", "サイズ", "size"]
        self.dictionary["INT"] = ["INT", "いんてりじぇんす", "インテリジェンス", "いんと", "イント", "intelligence"]
        self.dictionary["EDU"] = ["EDU", "えでゅけーしょん", "エデュケーション", "えでゅ", "エデュ", "education"]
        self.dictionary["アイデア"] = ["あいであ", "アイデア", "あいでぃあ", "アイディア"]
        self.dictionary["幸運"] = ["こううん", "コウウン", "幸運", "幸うん", "こう運", "こーうん", "コーウン"]
        self.dictionary["知識"] = ["ちしき", "チシキ", "知識", "知しき", "ち識"]
        self.dictionary["回避"] = ["かいひ", "カイヒ", "回避", "回ひ", "かい避"]
        self.dictionary["キック"] = ["きっく", "キック"]
        self.dictionary["組み付き"] = ["くみつき", "クミツキ", "組み付き", "組みつき", "くみ付き", "組付き", "組つき"]
        self.dictionary["こぶし"] = ["こぶし", "コブシ", "拳"]
        self.dictionary["頭突き"] = ["ずつき", "ズツキ", "ず突き", "頭つき"]
        self.dictionary["投擲"] = ["とうてき", "トウテキ", "投擲", "投てき", "とう擲"]
        self.dictionary["マーシャルアーツ"] = ["まーしゃるあーつ", "マーシャルアーツ"]
        self.dictionary["拳銃"] = ["けんじゅう", "ケンジュウ", "拳銃", "拳じゅう", "けん銃"]
        self.dictionary["サブマシンガン"] = ["さぶましんがん", "サブマシンガン"]
        self.dictionary["ショットガン"] = ["しょっとがん", "ショットガン"]
        self.dictionary["マシンガン"] = ["ましんがん", "マシンガン"]
        self.dictionary["ライフル"] = ["らいふる", "ライフル"]
        self.dictionary["応急手当"] = ["おうきゅうてあて", "オウキュウテアテ", "応急手当", "応急てあて", "おうきゅう手当"]
        self.dictionary["鍵開け"] = ["かぎあけ", "カギアケ", "鍵開け", "鍵あけ", "かぎ開け"]
        self.dictionary["隠す"] = ["かくす", "カクス", "隠す"]
        self.dictionary["隠れる"] = ["かくれる", "カクレル", "隠れる"]
        self.dictionary["聞き耳"] = ["ききみみ", "キキミミ", "聞き耳", "聞きみみ", "きき耳", "聴き耳"]
        self.dictionary["忍び歩き"] = ["しのびあるき", "シノビアルキ", "忍び歩き", "忍びあるき", "しのび歩き", "偲び歩き"]
        self.dictionary["写真術"] = ["しゃしんじゅつ", "シャシンジュツ", "写真術", "写真じゅつ", "しゃ真術"]
        self.dictionary["精神分析"] = ["せいしんぶんせき", "セイシンブンセキ", "精神分析", "精神ぶんせき", "せいしん分析"]
        self.dictionary["追跡"] = ["ついせき", "ツイセキ", "追跡", "追せき", "つい跡"]
        self.dictionary["登攀"] = ["とうはん", "トウハン", "登はん", "とう攀", "登坂", "盗犯"]
        self.dictionary["図書館"] = ["としょかん", "トショカン", "図書館", "図書かん", "と書館"]
        self.dictionary["目星"] = ["めぼし", "メボシ", "目星", "目ぼし", "め星", "眼星"]
        self.dictionary["機械修理"] = ["きかいしゅうり", "キカイシュウリ", "機械修理", "機械しゅうり", "きかい修理"]
        self.dictionary["重機械操作"] = ["じゅうきかいそうさ", "ジュウキカイソウサ", "重機械操作", "重機械そうさ", "じゅうきかい操作"]
        self.dictionary["乗馬"] = ["じょうば", "ジョウバ", "乗馬", "乗ば", "じょう馬"]
        self.dictionary["水泳"] = ["すいえい", "スイエイ", "水泳", "水えい", "すい泳"]
        self.dictionary["跳躍"] = ["ちょうやく", "チョウヤク", "跳躍", "跳やく", "ちょう躍"]
        self.dictionary["電気修理"] = ["でんきしゅうり", "デンキシュウリ", "電気修理", "電気しゅうり", "でんき修理"]
        self.dictionary["ナビゲート"] = ["なびげーと", "ナビゲート"]
        self.dictionary["変装"] = ["へんそう", "ヘンソウ", "変そう", "へん装"]
        self.dictionary["言いくるめ"] = ["いいくるめ", "イイクルメ", "言いくるめ", "言い包め", "いい包め"]
        self.dictionary["信用"] = ["しんよう", "シンヨウ", "信用", "信よう", "しん用"]
        self.dictionary["説得"] = ["せっとく", "セットク", "説得", "説とく", "せっ得"]
        self.dictionary["値切り"] = ["ねぎり", "ネギリ", "値切り", "値きり", "ね切り"]
        self.dictionary["母国語"] = ["ぼこくご", "ボコクゴ", "母国語", "母国ご", "ぼこく語", "言語"]
        self.dictionary["医学"] = ["いがく", "イガク", "医学", "医がく", "い学"]
        self.dictionary["オカルト"] = ["おかると", "オカルト"]
        self.dictionary["化学"] = ["かがく", "カガク", "化学", "化がく", "か学", "科学", "ばけがく"]
        self.dictionary["クトゥルフ神話"] = ["くとぅるふしんわ", "クトゥルフシンワ", "クトゥルフ神話", "クトゥルフ神わ", "クトゥルフしん話"]
        self.dictionary["経理"] = ["けいり", "ケイリ", "経理", "経り", "けい理"]
        self.dictionary["考古学"] = ["こうこがく", "コウコガク", "考古学", "考古がく", "こうこ学"]
        self.dictionary["コンピューター"] = ["こんぴゅーたー", "コンピューター", "こんぴゅーた", "コンピュータ", "パソコン"]
        self.dictionary["心理学"] = ["しんりがく", "シンリガク", "心理学", "心理がく", "しんり学"]
        self.dictionary["人類学"] = ["じんるいがく", "ジンルイガク", "人類学", "人類がく", "じんるい学"]
        self.dictionary["生物学"] = ["せいぶつがく", "セイブツガク", "生物学", "生物がく", "せいぶつ学"]
        self.dictionary["地質学"] = ["ちしつがく", "チシツガク", "地質学", "地質がく", "ちしつ学"]
        self.dictionary["電子工学"] = ["でんしこうがく", "デンシコウガク", "電子工学", "電子こうがく", "でんし工学"]
        self.dictionary["天文学"] = ["てんもんがく", "テンモンガク", "天文学", "天文がく", "てんもん学"]
        self.dictionary["博物学"] = ["はくぶつがく", "ハクブツガク", "博物学", "博物がく", "はくぶつ学"]
        self.dictionary["物理学"] = ["ぶつりがく", "ブツリガク", "物理学", "物理がく", "ぶつり学"]
        self.dictionary["法律"] = ["ほうりつ", "ホウリツ", "法律", "法りつ", "ほう律"]
        self.dictionary["薬学"] = ["やくがく", "ヤクガク", "薬学", "薬がく", "やく学"]
        self.dictionary["歴史"] = ["れきし", "レキシ", "歴史", "歴し", "れき史"]
        self.dictionary["日本語"] = ["にほんご", "ニホンゴ", "日本語", "日本ご", "にほん語"]
        self.dictionary["英語"] = ["えいご", "エイゴ", "英語", "英ご", "えい語"]
        self.dictionary["ラテン語"] = ["らてんご", "ラテンゴ", "ラテン語", "ラテンご"]
        self.dictionary["管楽器"] = ["かんがっき", "カンガッキ", "管楽器", "管楽き", "かん楽器"]
        self.dictionary["弦楽器"] = ["げんがっき", "ゲンガッキ", "弦楽器", "弦楽き", "げん楽器"]
        self.dictionary["打楽器"] = ["だがっき", "ダガッキ", "打楽器", "打楽き", "だ楽器"]
        self.dictionary["鍵盤楽器"] = ["けんばんがっき", "ケンバンガッキ", "鍵盤楽器", "鍵盤がっき", "けんばん楽器"]
        self.dictionary["音楽知識"] = ["おんがくちしき", "オンガクチシキ", "音楽知識", "音楽ちしき", "おんがく知識"]
        self.dictionary["陶芸"] = ["とうげい", "トウゲイ", "陶芸", "陶げい", "とう芸"]
        self.dictionary["製本"] = ["せいほん", "セイホン", "製本", "製ほん", "せい本"]
        self.dictionary["衣装制作"] = ["いしょうせいさく", "イショウセイサク", "衣装制作", "衣装せいさく", "いしょう制作"]
        self.dictionary["装飾芸術"] = ["そうしょくげいじゅつ", "ソウショクゲイジュツ", "装飾芸術", "装飾げいじゅつ", "そうしょく芸術"]
        self.dictionary["古書修復"] = ["こしょしゅうふく", "コショシュウフク", "古書修復", "古書しゅうふく", "こしょ修復"]
        self.__create_keywords()

    def __registration_of_similar_words(self, keywords: SearchKeyword):
        # main
        if keywords.search_results.main_name in self.dictionary:
            keywords.main_keyword.append(keywords.search_results.main_name)
            keywords.main_keyword.add(self.dictionary[keywords.search_results.main_name])
        else:
            keywords.main_keyword.append(keywords.search_results.main_name)
        # sub
        if keywords.search_results.sub_name in self.dictionary:
            keywords.sub_keyword.append(keywords.search_results.sub_name)
            keywords.sub_keyword.add(self.dictionary[keywords.search_results.sub_name])
        else:
            keywords.sub_keyword.append(keywords.search_results.sub_name)

        self.search_keywords.append(keywords)
        return self

    def __create_keywords(self):
        # SAN値
        changed_initial_value = 1
        skill_type = 1
        skill_current_value = self.investigator.sanity_points.current
        keywords = SearchKeyword().set_initialize("sanity_points", "SAN", "", changed_initial_value, skill_type, skill_current_value)
        self.__registration_of_similar_words(keywords)

        # 特徴
        exclusion_keys = ["hit_points", "magic_points", "initial_sanity"] # 除外キー
        for key in self.investigator.characteristics.keys():
            if not key in exclusion_keys:
                ability_set = self.investigator.characteristics[key]
                changed_initial_value = 1 if ability_set.base != ability_set.current else 0
                skill_type = 1
                skill_current_value = ability_set.current
                keywords = SearchKeyword().set_initialize(key, ability_set.ability_name, "", changed_initial_value, skill_type, skill_current_value)
                self.__registration_of_similar_words(keywords)

        # 戦闘技能
        for key in self.investigator.combat_skills.keys():
            skill_set = self.investigator.combat_skills[key]
            changed_initial_value = 1 if skill_set.base != skill_set.current else 0
            skill_type = 1 if skill_set.skill_type == "additions" else 0
            skill_current_value = skill_set.current
            keywords = SearchKeyword().set_initialize(key, skill_set.skill_name, skill_set.skill_subname, changed_initial_value, skill_type, skill_current_value)
            self.__registration_of_similar_words(keywords)

        # 探索技能
        for key in self.investigator.search_skills.keys():
            skill_set = self.investigator.search_skills[key]
            changed_initial_value = 1 if skill_set.base != skill_set.current else 0
            skill_type = 1 if skill_set.skill_type == "additions" else 0
            skill_current_value = skill_set.current
            keywords = SearchKeyword().set_initialize(key, skill_set.skill_name, skill_set.skill_subname, changed_initial_value, skill_type, skill_current_value)
            self.__registration_of_similar_words(keywords)

        # 行動技能
        for key in self.investigator.behavioral_skills.keys():
            skill_set = self.investigator.behavioral_skills[key]
            changed_initial_value = 1 if skill_set.base != skill_set.current else 0
            skill_type = 1 if skill_set.skill_type == "additions" else 0
            skill_current_value = skill_set.current
            keywords = SearchKeyword().set_initialize(key, skill_set.skill_name, skill_set.skill_subname, changed_initial_value, skill_type, skill_current_value)
            self.__registration_of_similar_words(keywords)

        # 交渉技能
        for key in self.investigator.negotiation_skills.keys():
            skill_set = self.investigator.negotiation_skills[key]
            changed_initial_value = 1 if skill_set.base != skill_set.current else 0
            skill_type = 1 if skill_set.skill_type == "additions" else 0
            skill_current_value = skill_set.current
            keywords = SearchKeyword().set_initialize(key, skill_set.skill_name, skill_set.skill_subname, changed_initial_value, skill_type, skill_current_value)
            self.__registration_of_similar_words(keywords)

        # 知識技能
        for key in self.investigator.knowledge_skills.keys():
            skill_set = self.investigator.knowledge_skills[key]
            changed_initial_value = 1 if skill_set.base != skill_set.current else 0
            skill_type = 1 if skill_set.skill_type == "additions" else 0
            skill_current_value = skill_set.current
            keywords = SearchKeyword().set_initialize(key, skill_set.skill_name, skill_set.skill_subname, changed_initial_value, skill_type, skill_current_value)
            self.__registration_of_similar_words(keywords)

        return self

    def search(self, text: str) -> List[SearchResult]:
        result: List[SearchResult] = []
        # あらかじめ、あいまい単語辞書を作っておく。正しいキーワードをキーとし、類似ワードをリスト化する。
        # この時、メインとサブのどちらでも使う単語、使いそうな単語を全て入れておく。

        # それぞれ探索者キャラデータを元に、その都度検索対象データを生成する。（追加技能に対応するため必須）

        # 検索用語をメインとサブに分ける。分けられない場合は、メインもサブも両方同一検索用語で検索する。
        # （検索用語に「母国語」「母国語（日本語）」「日本語」と入れられる可能性を考慮する）
        # このため、基本的にサブの方が優先度が高い。

        # メイン検索リスト、サブ検索リストをそれぞれ「近似ワード」を全てレーベンシュタインディスタンスで編集距離を計測する。
        # この時、ノーマライズして、近似ワードと「同一は1」、「異なるものは0」とする。
        # 最大値を「スキルワード」別に保存する。
        # 「スキルワード」が0なものを除外し、それぞれ降順にならべて、一番先頭のスキルを対象とする。

        match = FuzzySearchInvestigatorSkills.SKILL_TITLE_SPLIT.search(text)
        if match:
            main_name = str(match.group(1))
            sub_name = str(match.group(3))
        else:
            main_name = text
            sub_name = text

        df = pd.DataFrame(columns=[
            "link_name", "main_name", "sub_name",
            "changed_initial_value", "skill_type", "skill_current_value",
            "max_main_distance", "max_sub_distance", 'sum_distance'
            ])

        for keywords in self.search_keywords:
            keywords.search(main_name, sub_name)
            #print(keywords.to_display_string())

            row = pd.Series(index=list(df.columns))
            row["link_name"] = str(keywords.search_results.link_name)
            row["main_name"] = str(keywords.search_results.main_name)
            row["sub_name"] = str(keywords.search_results.sub_name)
            row["changed_initial_value"] = int(keywords.search_results.changed_initial_value)
            row["skill_type"] = int(keywords.search_results.skill_type)
            row["skill_current_value"] = int(keywords.search_results.skill_current_value)
            row["max_main_distance"] = keywords.search_results.max_main_distance
            row["max_sub_distance"] = keywords.search_results.max_sub_distance
            row["sum_distance"] = keywords.search_results.sum_distance
            df = df.append(row, ignore_index=True)

        #df = df[~((df["max_main_distance"] == 0) & (df["max_sub_distance"] == 0))]
        df = df[(df["sum_distance"] != 0)]
        #df.sort_values(['max_sub_distance', "max_main_distance"], ascending=[False, False], inplace=True)
        #df.sort_values('sum_distance', ascending=False, inplace=True)
        df.sort_values(["sum_distance", "changed_initial_value", "skill_type", "skill_current_value"],
                ascending=[False, False, False, False], inplace=True)
        df.reset_index(drop=True, inplace=True)
        #print(df)

        for index, row in df.iterrows():
            newRow = SearchResult()
            newRow.link_name = str(row["link_name"])
            newRow.main_name = str(row["main_name"])
            newRow.sub_name = str(row["sub_name"])
            newRow.changed_initial_value = int(row["changed_initial_value"])
            newRow.skill_type = int(row["skill_type"])
            newRow.skill_current_value = int(row["skill_current_value"])
            newRow.max_main_distance = Decimal(str(row["max_main_distance"]))
            newRow.max_sub_distance = Decimal(str(row["max_sub_distance"]))
            newRow.sum_distance = Decimal(str(row["sum_distance"]))
            result.append(newRow)

        return result

    def get_skill_value(self, link_name: str) -> int:
        result: int = 0
        if "sanity_points" in link_name:
            result = int(self.investigator.sanity_points.current)
        elif link_name in self.investigator.characteristics.keys():
            result = int(self.investigator.characteristics[link_name].current)
        elif link_name in self.investigator.combat_skills.keys():
            result = int(self.investigator.combat_skills[link_name].current)
        elif link_name in self.investigator.search_skills.keys():
            result = int(self.investigator.search_skills[link_name].current)
        elif link_name in self.investigator.behavioral_skills.keys():
            result = int(self.investigator.behavioral_skills[link_name].current)
        elif link_name in self.investigator.negotiation_skills.keys():
            result = int(self.investigator.negotiation_skills[link_name].current)
        elif link_name in self.investigator.knowledge_skills.keys():
            result = int(self.investigator.knowledge_skills[link_name].current)
        else:
            result = -1
        return result
