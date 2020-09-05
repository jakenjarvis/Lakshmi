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
            "Key": "unique_key",
            "SiteUrl": "site_url",
            "所有者ID": "author_id",
            "所有者名": "author_name",
            "Active": "active",
            "名前": "name",
            "画像Url": "image_url",
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

    #def _sortRows(self):
    #    print(r"  Sort rows: unique_key")
    #    self.df.sort_values(by=[r"unique_key"], ascending=True, inplace=True)

    def mergeDataFrame(self, dataFrame):
        super().merge(dataFrame, r'unique_key')

    def organizeDataFrameColumns(self, dataFrame):
        return dataFrame[list(self.nomalColumnNames.values())]

    def load(self):
        return super().load(LakshmiCharactersSheet.SHEET_NAME)

    def save(self):
        return super().save(LakshmiCharactersSheet.SHEET_NAME)
