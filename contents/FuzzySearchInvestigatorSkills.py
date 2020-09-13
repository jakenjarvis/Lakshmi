#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from decimal import Decimal
from typing import List, Dict
from dataclasses import dataclass, fields, field

import pandas as pd

from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance

from contents.character.Investigator import Investigator

@dataclass
class OneWord():
    keyword: str

    distance: Decimal = field(default_factory=lambda: Decimal("0.0"))

    def calc(self, search_word: str):
        self.distance = Decimal("1.0") - Decimal(str(normalized_damerau_levenshtein_distance(self.keyword, search_word)))
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
        self.dictionary["目星"] = ["目ぼし", "め星"]

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

    def search(self, text: str) -> List[SearchKeyword]:
        result: List[SearchKeyword] = []
        # あらかじめ、あいまい単語辞書を作っておく。正しいキーワードをキーとし、類似ワードをリスト化する。
        # この時、メインとサブのどちらでも使う単語、使いそうな単語を全て入れておく。

        # それぞれ探索者キャラデータを元に、その都度検索対象データを生成する。（追加技能に対応するため必須）

        # TODO:検索用語を変換する。英字大文字変換、半角→全角変換
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
