#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

class TextFileManager():
    def __init__(self, fileName, defaultEncoding="utf-8", defaultErrors="strict"):
        self.__fileName = fileName
        self.__defaultEncoding = defaultEncoding
        self.__defaultErrors = defaultErrors

    def __createPathFolder(self):
        dirPath = os.path.dirname(self.__fileName)
        os.makedirs(dirPath, exist_ok=True)
        return self

    def save(self, value, force=False, encoding="", errors=""):
        try:
            self.__createPathFolder()
            if force and os.path.isfile(self.__fileName):
                os.remove(self.__fileName)
                print("上書き作成: " + self.__fileName)

            if encoding == "":
                encoding = self.__defaultEncoding

            if errors == "":
                errors = self.__defaultErrors

            with open(self.__fileName, "w", encoding=encoding, errors=errors) as file:
                file.write(value)
        except Exception as e:
            print("Textファイルの書き込みに失敗しました: " + self.__fileName + " , " + str(e))

    def load(self, encoding="", errors=""):
        result = ""
        try:
            if encoding == "":
                encoding = self.__defaultEncoding

            if errors == "":
                errors = self.__defaultErrors

            with open(self.__fileName, "r", encoding=encoding, errors=errors) as file:
                result = file.read()
        except Exception as e:
            print("Textファイルの読み込みに失敗しました: " + self.__fileName + " , " + str(e))
        return result

