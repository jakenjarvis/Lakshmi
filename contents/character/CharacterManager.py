#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict
from distutils.util import strtobool
import requests

import discord
from discord.ext import commands

import LakshmiErrors
from contents.character.Investigator import Investigator
from contents.character.AbstractCharacterGetter import AbstractCharacterGetter
from contents.character.CharacterVampireBloodNetGetter import CharacterVampireBloodNetGetter
from contents.character.CharactersSheetController import CharactersSheetController
from contents.character.LakshmiCharactersSheetRecord import LakshmiCharactersSheetRecord

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
            raise LakshmiErrors.UnsupportedSitesException()
        return target_instance.request(instance, site_url)

    def is_image_url(self, url: str) -> bool:
        result = False
        try:
            response = requests.head(url)
            result = "image" in str(response.headers["content-type"])
        except Exception as e:
            result = False
        return result

    def character_add(self, context: commands.Context, url: str) -> Investigator:
        result = Investigator()

        if not self.request(result, url):
            raise LakshmiErrors.haracterNotFoundException()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        # もし画像を見つけたらイメージ画像として採用する。(複数ある場合は最後のもの)
        image_url = ""
        for attachment in context.message.attachments:
            print(attachment)
            temp_image_url = str(attachment.url)
            if self.is_image_url(temp_image_url):
                image_url = temp_image_url

        df = self.bot.storage.sheet_controller.find_character_by_site_info(author_id, result.site_id1, result.site_id2, result.site_url)
        if len(df) == 0:
            # 新規
            result.unique_id = self.bot.storage.sheet_controller.assign_unique_id(result.site_id1, result.site_id2, result.site_url)
            result.author_id = author_id
            result.author_name = author_name
            result.active = False
            result.image_url = image_url
        else:
            # 登録済み
            result.unique_id = str(df["unique_id"].values[0])
            result.author_id = author_id
            result.author_name = author_name
            result.active = strtobool(df["active"].values[0])
            if len(image_url) >= 1:
                result.image_url = image_url
            else:
                result.image_url = str(df["character_image_url"].values[0])

        record = LakshmiCharactersSheetRecord()
        record.set_values_by_investigator(result)
        self.bot.storage.sheet_controller.merge_character_by_unique_id(record)
        self.bot.storage.sheet_controller.save()
        return result

    def character_list(self, context: commands.Context) -> List[LakshmiCharactersSheetRecord]:
        result = []

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.bot.storage.sheet_controller.find_characters_by_author_id(author_id)
        if len(df) >= 1:
            # Sort
            df = df.sort_values('unique_id', ascending=True)
            # 1件以上あり
            for index, row in df.iterrows():
                record = LakshmiCharactersSheetRecord()
                record.set_values(
                    row["unique_id"],
                    row["site_id1"],
                    row["site_id2"],
                    row["site_url"],
                    row["character_name"],
                    row["character_image_url"],
                    author_id,
                    author_name,
                    row["active"],
                )
                result.append(record)
        return result

    def character_change(self, context: commands.Context, unique_id: str) -> LakshmiCharactersSheetRecord:
        result = LakshmiCharactersSheetRecord()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.bot.storage.sheet_controller.find_character_by_unique_id(author_id, unique_id)
        if len(df) == 0:
            # 登録がない
            raise LakshmiErrors.CharacterNotFoundException()

        self.bot.storage.sheet_controller.set_inactive_all_character_by_author_id(author_id)

        index = int(df.index[0])
        result.set_values(
            df["unique_id"].values[0],
            df["site_id1"].values[0],
            df["site_id2"].values[0],
            df["site_url"].values[0],
            df["character_name"].values[0],
            df["character_image_url"].values[0],
            author_id,
            author_name,
            True,
        )
        self.bot.storage.sheet_controller.update_character_by_index(index, result)
        self.bot.storage.sheet_controller.save()
        return result

    def set_image(self, context: commands.Context, unique_id: str, image_url: str) -> LakshmiCharactersSheetRecord:
        result = LakshmiCharactersSheetRecord()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.bot.storage.sheet_controller.find_character_by_unique_id(author_id, unique_id)
        if len(df) == 0:
            # 登録がない
            raise LakshmiErrors.CharacterNotFoundException()

        if not self.is_image_url(image_url):
            raise LakshmiErrors.ImageNotFoundException()

        index = int(df.index[0])
        result.set_values(
            df["unique_id"].values[0],
            df["site_id1"].values[0],
            df["site_id2"].values[0],
            df["site_url"].values[0],
            df["character_name"].values[0],
            image_url,
            author_id,
            author_name,
            df["active"].values[0],
        )
        self.bot.storage.sheet_controller.update_character_by_index(index, result)
        self.bot.storage.sheet_controller.save()
        return result

    def info_full(self, context: commands.Context, unique_id: str) -> Investigator:
        result = Investigator()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.bot.storage.sheet_controller.find_character_by_unique_id(author_id, unique_id)
        if len(df) == 0:
            # 登録がない
            raise LakshmiErrors.CharacterNotFoundException()

        # 登録済み
        site_url = str(df["site_url"].values[0])
        if not self.request(result, site_url):
            # TODO: delete sheet char
            raise LakshmiErrors.CharacterNotFoundException()

        # TODO:
        result.image_url = str(df["character_image_url"].values[0])

        return result
