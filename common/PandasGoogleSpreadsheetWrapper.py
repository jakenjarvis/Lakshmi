#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import csv

import numpy as np
import pandas as pd

from gspread_pandas import Spread, Client

from common.PandasWrapperBase import PandasWrapperBase
from common.GoogleCredentialsManager import GoogleCredentialsManager

class PandasGoogleSpreadsheetWrapper(PandasWrapperBase):
    def __init__(self, credentialsManager, spreadsheetId, dataFrame=None):
        super().__init__(dataFrame)
        self.__credentialsManager = credentialsManager
        self.__id = spreadsheetId
        self.__spreadsheet = Spread(spread=self.__id, creds=self.__credentialsManager.credentials)

    @property
    def credentialsManager(self):
        return self.__credentialsManager

    @property
    def spreadsheetId(self):
        return self.__id

    @property
    def spreadsheet(self):
        return self.__spreadsheet

    @property
    def active_sheet(self):
        return self.__spreadsheet.sheet

    def load(self, filePath):
        # filePath = SheetName
        print("Load GoogleSpreadsheet: " + str(self.__id) + " [" + str(filePath) + "]")
        self.onLoadPreprocessing(self.df)
        df = self.__spreadsheet.sheet_to_df(index=False, sheet=filePath)
        self.setDataFrame(df)
        print("  Loaded Length: " + str(len(self.df.index)))
        self.onLoadPostprocessing(self.df)
        return self

    def save(self, filePath):
        # filePath = SheetName
        print("Save GoogleSpreadsheet: " + str(self.__id) + " [" + str(filePath) + "]")
        self.onSavePreprocessing(self.df)
        self.__spreadsheet.open_sheet(filePath, create=True)
        self.__spreadsheet.df_to_sheet(df=self.df, index=False, headers=True, start='A1', replace=True)
        print("  Saved Length : " + str(len(self.df.index)))
        self.onSavePostprocessing(self.df)
        return self
