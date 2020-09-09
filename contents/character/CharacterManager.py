#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict
from distutils.util import strtobool
import copy
import aiohttp
import asyncio
import datetime
import pytz

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
        self.__sheet_controller: CharactersSheetController = self.bot.storage.sheet_controller
        self.__investigators: Dict[str, Investigator] = self.bot.storage.investigators

        # 対応サイトの追加
        self.instances: List[AbstractCharacterGetter] = []
        self.instances.append(CharacterVampireBloodNetGetter())

        self.save_flag = False

    def __get_instance_of_getter(self, site_url: str) -> AbstractCharacterGetter:
        result = None
        for instance in self.instances:
            if instance.is_detect_url(site_url):
                result = instance
                break
        return result

    async def register_investigator_in_cache(self, investigator: Investigator):
        self.__investigators[investigator.site_url] = investigator

    async def request(self, site_url: str) -> Investigator:
        result = None
        cache_investigator: Investigator = None
        is_cache = False

        if site_url in self.__investigators:
            # キャッシュに存在する
            cache_investigator = self.__investigators[site_url]
            if self.bot.storage.lexicon.get_jst_datetime_now() <= cache_investigator.created_at + datetime.timedelta(minutes=5):
                is_cache = True

        if is_cache:
            # キャッシュを返却
            result = copy.deepcopy(cache_investigator)
        else:
            # サイト取得
            getter = self.__get_instance_of_getter(site_url)
            if not getter:
                raise LakshmiErrors.UnsupportedSitesException()

            result = Investigator()
            if not await getter.request(result, site_url):
                raise LakshmiErrors.CharacterNotFoundException()
        return result

    async def background_save(self):
        if not self.save_flag:
            self.save_flag = True
            self.bot.loop.create_task(self.__background_save_task())

    async def __background_save_task(self):
        await asyncio.sleep(3)
        await self.bot.wait_until_ready()
        self.__sheet_controller.save()
        self.save_flag = False

    async def is_image_url(self, url: str) -> bool:
        result = False
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(url) as response:
                    if response.status == 200:
                        result = "image" in str(response.headers["content-type"])
        except Exception as e:
            result = False
        return result

    async def add_character(self, context: commands.Context, url: str) -> Investigator:
        result = await self.request(url)

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        # もし画像を見つけたらイメージ画像として採用する。(複数ある場合は最後のもの)
        image_url = ""
        for attachment in context.message.attachments:
            print(attachment)
            temp_image_url = str(attachment.url)
            if await self.is_image_url(temp_image_url):
                image_url = temp_image_url

        df = self.__sheet_controller.find_character_by_site_info(author_id, result.site_id1, result.site_id2, result.site_url)
        if len(df) == 0:
            # 新規
            result.unique_id = self.__sheet_controller.assign_unique_id(result.site_id1, result.site_id2, result.site_url)
            result.author_id = author_id
            result.author_name = author_name
            result.active = False
            result.lost = False
            result.image_url = image_url
        else:
            # 登録済み
            result.unique_id = str(df["unique_id"].values[0])
            result.author_id = author_id
            result.author_name = author_name
            result.active = strtobool(df["active"].values[0])
            result.lost = strtobool(df["lost"].values[0])
            if len(image_url) >= 1:
                result.image_url = image_url
            else:
                result.image_url = str(df["character_image_url"].values[0])

        record = LakshmiCharactersSheetRecord()
        record.set_values_by_investigator(result)
        self.__sheet_controller.merge_character_by_unique_id(record)

        # NOTE: self.__sheet_controllerのfind等からsaveまでの間にawait処理が入らないように注意。
        await self.register_investigator_in_cache(result)
        await self.background_save()
        return result

    async def delete_character(self, context: commands.Context, unique_id: str) -> LakshmiCharactersSheetRecord:
        result = LakshmiCharactersSheetRecord()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.__sheet_controller.find_character_by_unique_id(author_id, unique_id)
        if len(df) == 0:
            # 登録がない
            raise LakshmiErrors.CharacterNotFoundException()

        result.set_values_by_dataframe(df)
        result.author_id = author_id
        result.author_name = author_name

        index = int(df.index[0])
        self.__sheet_controller.delete_character_by_index(index)

        # NOTE: self.__sheet_controllerのfind等からsaveまでの間にawait処理が入らないように注意。
        await self.background_save()
        return result

    async def get_character_list(self, context: commands.Context) -> List[LakshmiCharactersSheetRecord]:
        result = []

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.__sheet_controller.find_characters_by_author_id(author_id)
        if len(df) >= 1:
            # Sort
            df = df.sort_values('unique_id', ascending=True)
            # 1件以上あり
            for index, row in df.iterrows():
                record = LakshmiCharactersSheetRecord()
                record.set_values_by_series(row)
                record.author_id = author_id
                record.author_name = author_name
                result.append(record)
        return result

    async def set_character_active(self, context: commands.Context, unique_id: str) -> LakshmiCharactersSheetRecord:
        result = LakshmiCharactersSheetRecord()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.__sheet_controller.find_character_by_unique_id(author_id, unique_id)
        if len(df) == 0:
            # 登録がない
            raise LakshmiErrors.CharacterNotFoundException()

        result.set_values_by_dataframe(df)
        result.author_id = author_id
        result.author_name = author_name
        result.active = True

        self.__sheet_controller.set_inactive_all_character_by_author_id(author_id)

        index = int(df.index[0])
        self.__sheet_controller.update_character_by_index(index, result)

        # NOTE: self.__sheet_controllerのfind等からsaveまでの間にawait処理が入らないように注意。
        await self.background_save()
        return result

    async def set_character_image(self, context: commands.Context, unique_id: str, image_url: str) -> LakshmiCharactersSheetRecord:
        result = LakshmiCharactersSheetRecord()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        #NOTE: find_character_by_unique_idよりも前にis_image_urlする。
        if not await self.is_image_url(image_url):
            raise LakshmiErrors.ImageNotFoundException()

        df = self.__sheet_controller.find_character_by_unique_id(author_id, unique_id)
        if len(df) == 0:
            # 登録がない
            raise LakshmiErrors.CharacterNotFoundException()

        result.set_values_by_dataframe(df)
        result.character_image_url = image_url
        result.author_id = author_id
        result.author_name = author_name

        index = int(df.index[0])
        self.__sheet_controller.update_character_by_index(index, result)

        # NOTE: self.__sheet_controllerのfind等からsaveまでの間にawait処理が入らないように注意。
        await self.background_save()
        return result

    async def set_character_lost(self, context: commands.Context, unique_id: str) -> LakshmiCharactersSheetRecord:
        result = LakshmiCharactersSheetRecord()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.__sheet_controller.find_character_by_unique_id(author_id, unique_id)
        if len(df) == 0:
            # 登録がない
            raise LakshmiErrors.CharacterNotFoundException()

        result.set_values_by_dataframe(df)
        result.author_id = author_id
        result.author_name = author_name
        result.lost = True

        index = int(df.index[0])
        self.__sheet_controller.update_character_by_index(index, result)

        # NOTE: self.__sheet_controllerのfind等からsaveまでの間にawait処理が入らないように注意。
        await self.background_save()
        return result

    async def get_character_information(self, context: commands.Context, unique_id: str) -> Investigator:
        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.__sheet_controller.find_character_by_unique_id(author_id, unique_id)
        if len(df) == 0:
            # 登録がない
            raise LakshmiErrors.CharacterNotFoundException()

        # 登録済み
        record = LakshmiCharactersSheetRecord()
        record.set_values_by_dataframe(df)
        record.author_id = author_id
        record.author_name = author_name

        #NOTE: find_character_by_unique_idの後だが、background_saveしないのでOKとする。
        result = await self.request(record.site_url)
        self.__sheet_controller.set_investigator_by_record(result, record)

        await self.register_investigator_in_cache(result)
        return result
