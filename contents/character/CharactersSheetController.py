#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from distutils.util import strtobool

import pandas as pd
import ulid

from contents.character.LakshmiCharactersSheet import LakshmiCharactersSheet
from contents.character.LakshmiCharactersSheetRecord import LakshmiCharactersSheetRecord
from contents.character.Investigator import Investigator

class CharactersSheetController():
    def __init__(self, pandasheet: LakshmiCharactersSheet):
        self.pandasheet = pandasheet

    @property
    def df(self):
        return self.pandasheet.df

    def load(self):
        self.pandasheet.load()
        return self

    def save(self):
        self.pandasheet.save()
        return self

    def set_investigator_by_record(self, target: Investigator, record: LakshmiCharactersSheetRecord, overwrite=False):
        target.unique_id = str(record.unique_id)
        target.site_id1 = str(record.site_id1) if overwrite else target.site_id1
        target.site_id2 = str(record.site_id2) if overwrite else target.site_id2
        target.site_url = str(record.site_url) if overwrite else target.site_url
        target.personal_data.name = str(record.character_name) if overwrite else target.personal_data.name
        target.image_url = str(record.character_image_url)
        target.author_id = str(record.author_id)
        target.author_name = str(record.author_name)
        target.active = bool(record.active)
        target.lost = bool(record.lost)
        return self

    def set_investigator_by_dataframe(self, target: Investigator, df: pd.DataFrame, overwrite=False):
        target.unique_id = str(df["unique_id"].values[0])
        target.site_id1 = str(df["site_id1"].values[0]) if overwrite else target.site_id1
        target.site_id2 = str(df["site_id2"].values[0]) if overwrite else target.site_id2
        target.site_url = str(df["site_url"].values[0]) if overwrite else target.site_url
        target.personal_data.name = str(df["character_name"].values[0]) if overwrite else target.personal_data.name
        target.image_url = str(df["character_image_url"].values[0])
        target.author_id = str(df["author_id"].values[0])
        target.author_name = str(df["author_name"].values[0])
        target.active = strtobool(str(df["active"].values[0]))
        target.lost = strtobool(str(df["lost"].values[0]))
        return self

    def set_investigator_by_series(self, target: Investigator, row: pd.Series, overwrite=False):
        target.unique_id = str(row["unique_id"])
        target.site_id1 = str(row["site_id1"]) if overwrite else target.site_id1
        target.site_id2 = str(row["site_id2"]) if overwrite else target.site_id2
        target.site_url = str(row["site_url"]) if overwrite else target.site_url
        target.personal_data.name = str(row["character_name"]) if overwrite else target.personal_data.name
        target.image_url = str(row["character_image_url"])
        target.author_id = str(row["author_id"])
        target.author_name = str(row["author_name"])
        target.active = strtobool(str(row["active"]))
        target.lost = strtobool(str(row["lost"]))
        return self

    def insert_character(self, record: LakshmiCharactersSheetRecord):
        row = self.pandasheet.createRowSeries()
        row["unique_id"] = record.unique_id
        row["site_id1"] = record.site_id1
        row["site_id2"] = record.site_id2
        row["site_url"] = record.site_url
        row["character_name"] = record.character_name
        row["character_image_url"] = record.character_image_url
        row["author_id"] = record.author_id
        row["author_name"] = record.author_name
        row["active"] = record.get_active_to_string()
        row["lost"] = record.get_lost_to_string()
        self.pandasheet.appendRow(row)
        return self

    def update_character_by_index(self, index, record: LakshmiCharactersSheetRecord):
        row = pd.Series(self.pandasheet.df.iloc[index])
        row["unique_id"] = record.unique_id
        row["site_id1"] = record.site_id1
        row["site_id2"] = record.site_id2
        row["site_url"] = record.site_url
        row["character_name"] = record.character_name
        row["character_image_url"] = record.character_image_url
        row["author_id"] = record.author_id
        row["author_name"] = record.author_name
        row["active"] = record.get_active_to_string()
        row["lost"] = record.get_lost_to_string()
        self.pandasheet.df.iloc[index] = row
        return self

    def delete_character_by_index(self, index):
        self.pandasheet.df.drop(self.pandasheet.df.index[[index]], inplace=True)
        self.pandasheet.df.reset_index(drop=True, inplace=True)
        return self

    def merge_character_by_unique_id(self, record: LakshmiCharactersSheetRecord):
        # update / insert
        df = self.find_character_by_unique_id(record.author_id, record.unique_id)
        if len(df) == 0:
            # insert
            self.insert_character(record)
        else:
            # update
            target_index = int(df.index[0])
            self.update_character_by_index(target_index, record)

    def set_inactive_all_character_by_author_id(self, author_id: str):
        self.pandasheet.df.active[self.pandasheet.df.author_id == author_id] = "FALSE"

    def assign_unique_id(self, site_id1: str, site_id2: str, site_url: str) -> str:
        result = ""
        # NOTE: ここでは、author_idで絞り込まない。
        where = FuzzyWhere(self.pandasheet.df).or_site_id1(site_id1).or_site_id2(site_id2).or_site_url(site_url).build()
        df = self.pandasheet.df[where]
        if len(df) >= 1:
            # 既知のキャラクター。既存IDの割り当て
            result = str(df["unique_id"].values[0])
        else:
            # 未知のキャラクター。新規IDの割り当て
            result = ulid.new()
        return result

    def find_character_by_record(self, record: LakshmiCharactersSheetRecord) -> pd.DataFrame:
        where = FuzzyWhere(self.pandasheet.df) \
            .or_unique_id(record.unique_id) \
            .or_site_id1(record.site_id1) \
            .or_site_id2(record.site_id2) \
            .or_site_url(record.site_url).build()
        # NOTE: この時点で、whereがNoneであることは想定しない（どれか指定があるはず）
        return self.pandasheet.df[(self.pandasheet.df["author_id"] == record.author_id) & where]

    def find_character_by_site_info(self, author_id: str, site_id1: str, site_id2: str, site_url: str) -> pd.DataFrame:
        where = FuzzyWhere(self.pandasheet.df).or_site_id1(site_id1).or_site_id2(site_id2).or_site_url(site_url).build()
        # NOTE: この時点で、whereがNoneであることは想定しない（どれか指定があるはず）
        return self.pandasheet.df[(self.pandasheet.df["author_id"] == author_id) & where]

    def find_character_by_unique_id(self, author_id: str, unique_id: str) -> pd.DataFrame:
        return self.pandasheet.df[
            (self.pandasheet.df["author_id"] == author_id) & (self.pandasheet.df["unique_id"] == unique_id)
        ]

    def find_characters_by_author_id(self, author_id: str) -> pd.DataFrame:
        return self.pandasheet.df[self.pandasheet.df["author_id"].isin([author_id])]

    def find_active_character_by_author_id(self, author_id: str) -> pd.DataFrame:
        return self.pandasheet.df[
            (self.pandasheet.df["author_id"] == author_id) & (self.pandasheet.df["active"] == "TRUE")
        ]


class FuzzyWhere():
    def __init__(self, df):
        self.df = df
        # 比較結果初期値としてゼロ検索結果を詰めておく。
        self.__where = (self.df["unique_id"] == "]|>-!Never match forever!-<|[")

    def or_unique_id(self, unique_id: str):
        if len(unique_id) >= 1:
            self.__where |= (self.df["unique_id"] == str(unique_id))
        return self

    def or_site_id1(self, site_id1: str):
        if len(site_id1) >= 1:
            self.__where |= (self.df["site_id1"] == str(site_id1))
        return self

    def or_site_id2(self, site_id2: str):
        if len(site_id2) >= 1:
            self.__where |= (self.df["site_id2"] == str(site_id2))
        return self

    def or_site_url(self, site_url: str):
        if len(site_url) >= 1:
            self.__where |= (self.df["site_url"] == str(site_url))
        return self

    def build(self):
        return self.__where
