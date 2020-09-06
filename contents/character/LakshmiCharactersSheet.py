#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pandas as pd

from common.PandasGoogleSpreadsheetWrapper import PandasGoogleSpreadsheetWrapper

class LakshmiCharactersSheet(PandasGoogleSpreadsheetWrapper):
    SHEET_NAME = "Characters"

    def __init__(self, credentialsManager, spreadsheetId, dataFrame=None):
        super().__init__(credentialsManager, spreadsheetId, dataFrame)

        self.nomalColumnNames = {
            "キャラクタID": "unique_id",
            "SiteId1": "site_id1",
            "SiteId2": "site_id2",
            "SiteUrl": "site_url",
            "キャラクター名": "character_name",
            "画像URL": "character_image_url",
            "所有者ID": "author_id",
            "所有者名": "author_name",
            "Active": "active",
        }
        self.reverseColumnNames = {v: k for k, v in self.nomalColumnNames.items()}

    def createDataFrame(self):
        super().createDataFrame(self.nomalColumnNames.values())

    def onLoadPreprocessing(self, df):
        pass

    def onLoadPostprocessing(self, df):
        self._renameColumnNamesToId()

    def onSavePreprocessing(self, df):
        #self._sortRows() # Save前にソートする。
        self._renameColumnNamesToName()

    def onSavePostprocessing(self, df):
        self._renameColumnNamesToId()

    def _renameColumnNamesToId(self):
        print(r"  Set ColumnNames to ID")
        self.df.rename(columns=self.nomalColumnNames, inplace=True)

    def _renameColumnNamesToName(self):
        print(r"  Set ColumnNames to Name")
        self.df.rename(columns=self.reverseColumnNames, inplace=True)

    def mergeDataFrame(self, dataFrame):
        super().merge(dataFrame, r'unique_id')

    def organizeDataFrameColumns(self, dataFrame):
        return dataFrame[list(self.nomalColumnNames.values())]

    def load(self):
        return super().load(LakshmiCharactersSheet.SHEET_NAME)

    def save(self):
        return super().save(LakshmiCharactersSheet.SHEET_NAME)
