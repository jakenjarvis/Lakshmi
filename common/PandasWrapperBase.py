#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

class PandasWrapperBase():
    def __init__(self, dataFrame=None):
        self.__dataFrame = dataFrame

    @property
    def df(self):
        return self.__dataFrame

    def setDataFrame(self, dataFrame):
        self.__dataFrame = dataFrame

    def createDataFrame(self, columns=[]):
        self.__dataFrame = pd.DataFrame(columns=list(columns))

    def createRowSeries(self):
        return pd.Series(index=list(self.__dataFrame.columns))

    def appendRow(self, row):
        # row: Series or Dict
        self.__dataFrame = self.__dataFrame.append(row, ignore_index=True)

    def onLoadPreprocessing(self, df):
        pass

    def onLoadPostprocessing(self, df):
        pass

    def onSavePreprocessing(self, df):
        pass

    def onSavePostprocessing(self, df):
        pass

    def load(self, filePath):
        self.onLoadPreprocessing(self.__dataFrame)
        pass
        self.onLoadPostprocessing(self.__dataFrame)
        return self

    def save(self, filePath):
        self.onSavePreprocessing(self.__dataFrame)
        pass
        self.onSavePostprocessing(self.__dataFrame)
        return self

    def merge(self, df_right, indexColumnName):
        # indexColumnNameをキーに、Update＆InsertでMergeしたDataFrameを返却する。

        df_left = self.__dataFrame
        # df_leftとdf_rightの差分抽出（df_rightにのみ存在する行DFを取得）
        df_diff = df_right[~df_right[indexColumnName].isin(df_left[indexColumnName])]
        #print(" df_diff Length : " + str(len(df_diff.index)))
        #print(df_diff)
        df_base = df_left.append(df_diff)

        # インデックスを割り当てる
        left_index = df_base.set_index(indexColumnName)
        right_index = df_right.set_index(indexColumnName)
        df_result = left_index.reindex(columns=left_index.columns.union(right_index.columns))
        # 更新
        df_result.update(right_index)
        df_result.reset_index(inplace=True)

        self.__dataFrame = df_result
        return self
