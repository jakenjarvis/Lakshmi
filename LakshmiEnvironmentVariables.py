#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import copy
import json

from common.TextFileManager import TextFileManager

class LakshmiEnvironmentVariables():
    def __init__(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.__basepath = os.path.abspath(os.path.join(current_path, r".credentials"))
        print(self.__basepath)

        # デフォルトスコープ
        self.__scopes = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/script.external_request',
            'https://www.googleapis.com/auth/script.send_mail',
            'https://www.googleapis.com/auth/spreadsheets'
            ]

    def get_google_credentials_scopes(self):
        return self.__scopes

    def get_google_credentials_json(self):
        # Service Account
        result = ""
        try:
            # Heroku環境
            result = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON_STRING'])
        except Exception as e:
            # ローカル環境
            path = os.path.abspath(os.path.join(self.__basepath, r"google-credentials.json"))
            result = json.loads(TextFileManager(path).load())
        return result

    def get_discord_token(self):
        # Discord Token
        result = ""
        try:
            # Heroku環境
            result = os.environ['DISCORD_TOKEN']
        except Exception as e:
            # ローカル環境
            path = os.path.abspath(os.path.join(self.__basepath, r"discord-token.txt"))
            result = TextFileManager(path).load()
        return result

    def get_spreadsheet_id(self):
        # Spreadsheet Id
        result = ""
        try:
            # Heroku環境
            result = os.environ['SPREADSHEET_ID']
        except Exception as e:
            # ローカル環境
            path = os.path.abspath(os.path.join(self.__basepath, r"spreadsheet-id.txt"))
            result = TextFileManager(path).load()
        return result

    def get_person_name_api_url(self):
        # person_name_api URL
        result = ""
        try:
            # Heroku環境
            result = os.environ['PERSON_NAME_API_URL']
        except Exception as e:
            # ローカル環境
            path = os.path.abspath(os.path.join(self.__basepath, r"person_name_api-url.txt"))
            result = TextFileManager(path).load()
        return result
