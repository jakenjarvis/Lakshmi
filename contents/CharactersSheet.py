#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pandas as pd

from common.PandasGoogleSpreadsheetWrapper import PandasGoogleSpreadsheetWrapper

class CharactersSheet(PandasGoogleSpreadsheetWrapper):
    def __init__(self, credentialsManager, spreadsheetId, dataFrame=None):
        super().__init__(credentialsManager, spreadsheetId, dataFrame)

        # TODO: 項目確認が必要
        self.nomalColumnNames = {
            "所有者ID": "authorId",
            "所有者名": "authorName",
            "Key": "uniqueKey",
            "Active": "active",
            "名前": "name",
            "SiteUrl": "siteUrl",
        }
        self.reverseColumnNames = {v: k for k, v in self.nomalColumnNames.items()}

    def createDataFrame(self):
        super().createDataFrame(self.nomalColumnNames.values())

    def onLoadPreprocessing(self, df):
        pass

    def onLoadPostprocessing(self, df):
        self._renameColumnNamesToId()

    def onSavePreprocessing(self, df):
        self._sortRows() # Save前にソートする。
        self._renameColumnNamesToName()

    def onSavePostprocessing(self, df):
        self._renameColumnNamesToId()

    def _renameColumnNamesToId(self):
        print(r"  Set ColumnNames to ID")
        self.df.rename(columns=self.nomalColumnNames, inplace=True)

    def _renameColumnNamesToName(self):
        print(r"  Set ColumnNames to Name")
        self.df.rename(columns=self.reverseColumnNames, inplace=True)

    def _sortRows(self):
        print(r"  Sort rows: uniqueKey")
        self.df.sort_values(by=[r"uniqueKey"], ascending=True, inplace=True)

    def mergeDataFrame(self, dataFrame):
        super().merge(dataFrame, r'uniqueKey')

    def organizeDataFrameColumns(self, dataFrame):
        return dataFrame[list(self.nomalColumnNames.values())]
