#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict
from distutils.util import strtobool

import discord
from discord.ext import commands

from LakshmiErrors import UnsupportedSitesException
from contents.character.Investigator import Investigator
from contents.character.AbstractCharacterGetter import AbstractCharacterGetter
from contents.character.CharacterVampireBloodNetGetter import CharacterVampireBloodNetGetter
from LakshmiErrors import CharacterNotFoundException
from contents.character.CharactersSheetController import CharactersSheetController

class CharacterManager():
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        #self.bot.storage

        self.instances: List[AbstractCharacterGetter] = []
        # 対応サイトの追加
        self.instances.append(CharacterVampireBloodNetGetter())

    def get_target_instance(self, site_url: str) -> AbstractCharacterGetter:
        result = None
        for instance in self.instances:
            if instance.is_detect_url(site_url):
                result = instance
                break
        return result

    def request(self, instance: Investigator, site_url: str) -> bool:
        target_instance = self.get_target_instance(site_url)
        if not target_instance:
            raise UnsupportedSitesException()
        return target_instance.request(instance, site_url)



    def character_add(self, context: commands.Context, url: str) -> Investigator:
        result = Investigator()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        if not self.request(result, url):
            raise CharacterNotFoundException()

        df = self.bot.storage.sheet_controller.find_character_by_site_url(author_id, url)
        if len(df) == 0:
            # 新規
            result.unique_key = self.bot.storage.sheet_controller.assign_unique_key(url)
            result.author_id = author_id
            result.author_name = author_name
            result.active = False
            result.image_url = ""
            #print("ZZZZ1: " + str(character.active))
        else:
            # 登録済み
            result.unique_key = str(df["unique_key"].values[0])
            result.author_id = author_id
            result.author_name = author_name
            result.active = strtobool(df["active"].values[0])
            result.image_url = str(df["image_url"].values[0])
            #print("ZZZZ2: " + str(character.active))

        self.bot.storage.sheet_controller.merge_character_by_site_url(
            result.unique_key,
            result.site_url,
            result.author_id,
            result.author_name,
            result.active,
            result.name,
            result.image_url
            )

        self.bot.storage.sheet_controller.save()
        return result

    def character_list(self, context: commands.Context) -> List[Investigator]:
        result = []
        author_id = str(context.author.id)
        df = self.bot.storage.sheet_controller.find_characters_by_author_id(author_id)
        if len(df) >= 1:
            # Sort
            df = df.sort_values('unique_key', ascending=True)

            # 1件以上あり
            for index, row in df.iterrows():
                character = Investigator()
                character.unique_key = str(row['unique_key'])
                character.active = strtobool(row['active'])
                character.personal_data.name = str(row['name'])
                character.image_url = str(row['image_url'])
                result.append(character)
        return result

    def info_full(self, context: commands.Context, unique_key: str) -> Investigator:
        result = None

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.bot.storage.sheet_controller.find_character_by_unique_key(author_id, unique_key)
        if len(df) == 0:
            # 登録がない
            raise CharacterNotFoundException()

        # 登録済み
        result = Investigator()
        result.unique_key = str(df["unique_key"].values[0])
        result.author_id = author_id
        result.author_name = author_name
        result.active = strtobool(df["active"].values[0])
        result.image_url = str(df["image_url"].values[0])

        site_url = str(df["site_url"].values[0])
        if not self.request(result, site_url):
            # TODO: delete sheet char
            raise CharacterNotFoundException()

        return result
