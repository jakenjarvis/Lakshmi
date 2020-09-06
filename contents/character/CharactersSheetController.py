#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from distutils.util import strtobool

import pandas as pd
import ulid

from contents.character.LakshmiCharactersSheet import LakshmiCharactersSheet
from LakshmiEnvironmentVariables import LakshmiEnvironmentVariables
from common.GoogleCredentialsManager import GoogleCredentialsManager

class CharactersSheetController():
    def __init__(self, pandasheet: LakshmiCharactersSheet):
        self.pandasheet = pandasheet
        # TODO: 最後にロードしてから時間が経ってたら、再ロードする？
        # TODO: セーブロードのコントロール方法について検討
        #sheet.load()

    @property
    def df(self):
        return self.pandasheet.df

    def load(self):
        self.pandasheet.load()
        return self

    def save(self):
        self.pandasheet.save()
        return self

    def merge_character_by_site_url(self, unique_key, site_url, author_id, author_name, active, name, image_url):
        # update / insert
        target_index = -1
        # author_idとsite_urlが一致するものを検索
        df = self.pandasheet.df[
            (self.pandasheet.df["site_url"] == site_url) & (self.pandasheet.df["author_id"] == author_id)
        ]
        if len(df) == 0:
            # insert
            row = self.pandasheet.createRowSeries()
            row["unique_key"] = str(unique_key)
            row["site_url"] = str(site_url)
            row["author_id"] = str(author_id)
            row["author_name"] = str(author_name)
            row["active"] = "TRUE" if bool(active) else "FALSE"
            row["name"] = str(name)
            row["image_url"] = str(image_url)
            self.pandasheet.appendRow(row)
            #print("YYYY1: " + str(row["active"]))
        else:
            # update
            target_index = int(df.index[0])
            row = pd.Series(self.pandasheet.df.iloc[target_index])
            row["unique_key"] = str(unique_key)
            row["site_url"] = str(site_url)
            row["author_id"] = str(author_id)
            row["author_name"] = str(author_name)
            row["active"] = "TRUE" if bool(active) else "FALSE"
            row["name"] = str(name)
            row["image_url"] = str(image_url)
            self.pandasheet.df.iloc[target_index] = row
            #print("YYYY2: " + str(row["active"]))

    def assign_unique_key(self, site_url: str) -> str:
        result = ""
        df = self.pandasheet.df[self.pandasheet.df["site_url"] == site_url]
        if len(df) >= 1:
            # 既知のキャラクター。既存IDの割り当て
            result = str(df["unique_key"].values[0])
        else:
            # 未知のキャラクター。新規IDの割り当て
            result = ulid.new()
        return result

    def find_character_by_site_url(self, author_id: str, site_url: str) -> pd.DataFrame:
        return self.pandasheet.df[
            (self.pandasheet.df["author_id"] == author_id) & (self.pandasheet.df["site_url"] == site_url)
        ]

    def find_character_by_unique_key(self, author_id: str, unique_key: str) -> pd.DataFrame:
        return self.pandasheet.df[
            (self.pandasheet.df["author_id"] == author_id) & (self.pandasheet.df["unique_key"] == unique_key)
        ]

    def find_characters_by_author_id(self, author_id: str) -> pd.DataFrame:
        return self.pandasheet.df[self.pandasheet.df["author_id"].isin([author_id])]
