#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict

from LakshmiEnvironmentVariables import LakshmiEnvironmentVariables
from common.GoogleCredentialsManager import GoogleCredentialsManager
from contents.LakshmiLexicon import LakshmiLexicon
from contents.character.Investigator import Investigator
from contents.character.LakshmiCharactersSheet import LakshmiCharactersSheet
from contents.character.CharactersSheetController import CharactersSheetController

class LakshmiBrainStorage():
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

        self.__environment: LakshmiEnvironmentVariables = LakshmiEnvironmentVariables()

        # Lakshmi語彙
        self.__lexicon: LakshmiLexicon = LakshmiLexicon(bot)
        # 探索者キャッシュ
        self.__investigators: Dict[str, Investigator] = {} # key=site_url

        print("Start GoogleConnection.")
        self.__gcmanager: GoogleCredentialsManager = GoogleCredentialsManager(
            self.__environment.get_google_credentials_json(),
            self.__environment.get_google_credentials_scopes()
            )

        print("Start ServiceAccount Connection.")
        self.__gcmanager.getCredentials_FromServiceAccount()

        print("Start Access to spreadsheet.")
        self.__sheet_id: str = self.__environment.get_spreadsheet_id()
        self.__pandasheet: LakshmiCharactersSheet = LakshmiCharactersSheet(self.__gcmanager, self.__sheet_id)
        self.__sheet_controller: CharactersSheetController = CharactersSheetController(self.__pandasheet)
        self.__sheet_controller.load()
        print("End GoogleConnection.")

    @property
    def environment(self) -> LakshmiEnvironmentVariables:
        return self.__environment

    @property
    def lexicon(self) -> LakshmiLexicon:
        return self.__lexicon

    @property
    def investigators(self) -> Dict[str, Investigator]:
        return self.__investigators

    @property
    def gcmanager(self) -> GoogleCredentialsManager:
        return self.__gcmanager

    @property
    def sheet_id(self) -> str:
        return self.__sheet_id

    @property
    def pandasheet(self) -> LakshmiCharactersSheet:
        return self.__pandasheet

    @property
    def sheet_controller(self) -> CharactersSheetController:
        return self.__sheet_controller
