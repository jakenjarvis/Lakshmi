#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict
from dataclasses import dataclass, fields, field
from distutils.util import strtobool

import pandas as pd

from contents.character.Investigator import Investigator

@dataclass
class LakshmiCharactersSheetRecord:
    unique_id: str = ""             # キャラクタID

    site_id1: str = ""              # SiteId1
    site_id2: str = ""              # SiteId2

    site_url: str = ""              # SiteUrl

    character_name: str = ""        # キャラクター名
    character_image_url: str = ""   # 画像URL

    author_id: str = ""             # 所有者ID
    author_name: str = ""           # 所有者名

    active: bool = False            # Active
    lost: bool = False              # Lost

    def get_active_to_string(self) -> str:
        return "TRUE" if bool(self.active) else "FALSE"

    def set_active_from_string(self, value):
        if type(value) is bool:
            self.active = value
        else:
            self.active = strtobool(str(value))

    def get_lost_to_string(self) -> str:
        return "TRUE" if bool(self.lost) else "FALSE"

    def set_lost_from_string(self, value):
        if type(value) is bool:
            self.lost = value
        else:
            self.lost = strtobool(str(value))

    def set_values(self, unique_id, site_id1, site_id2, site_url, character_name, character_image_url, author_id, author_name, active, lost):
        self.unique_id = str(unique_id)
        self.site_id1 = str(site_id1)
        self.site_id2 = str(site_id2)
        self.site_url = str(site_url)
        self.character_name = str(character_name)
        self.character_image_url = str(character_image_url)
        self.author_id = str(author_id)
        self.author_name = str(author_name)
        self.set_active_from_string(active)
        self.set_lost_from_string(lost)
        return self

    def set_values_by_investigator(self, target: Investigator):
        return self.set_values(
            target.unique_id,
            target.site_id1,
            target.site_id2,
            target.site_url,
            target.character_name,
            target.character_image_url,
            target.author_id,
            target.author_name,
            target.active,
            target.lost,
        )

    def set_values_by_dataframe(self, df: pd.DataFrame):
        return self.set_values(
            df["unique_id"].values[0],
            df["site_id1"].values[0],
            df["site_id2"].values[0],
            df["site_url"].values[0],
            df["character_name"].values[0],
            df["character_image_url"].values[0],
            df["author_id"].values[0],
            df["author_name"].values[0],
            df["active"].values[0],
            df["lost"].values[0],
        )

    def set_values_by_series(self, row: pd.Series):
        return self.set_values(
            row["unique_id"],
            row["site_id1"],
            row["site_id2"],
            row["site_url"],
            row["character_name"],
            row["character_image_url"],
            row["author_id"],
            row["author_name"],
            row["active"],
            row["lost"],
        )

    def to_display_string(self):
        act = "●" if self.active else " "
        lst = "💀" if self.lost else ""
        return f"{act} {self.unique_id} : {lst}{self.character_name}"
