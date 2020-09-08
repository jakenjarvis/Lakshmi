#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict
from distutils.util import strtobool
import aiohttp
import asyncio

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

        # 対応サイトの追加
        self.instances: List[AbstractCharacterGetter] = []
        self.instances.append(CharacterVampireBloodNetGetter())

        self.save_flag = False

    def get_getter_instance(self, site_url: str) -> AbstractCharacterGetter:
        result = None
        for instance in self.instances:
            if instance.is_detect_url(site_url):
                result = instance
                break
        return result

    async def request(self, instance: Investigator, site_url: str) -> bool:
        target_instance = self.get_getter_instance(site_url)
        if not target_instance:
            raise LakshmiErrors.UnsupportedSitesException()
        return await target_instance.request(instance, site_url)

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

    async def character_add(self, context: commands.Context, url: str) -> Investigator:
        result = Investigator()

        if not await self.request(result, url):
            raise LakshmiErrors.haracterNotFoundException()

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
        await self.background_save()
        return result

    async def character_delete(self, context: commands.Context, unique_id: str) -> LakshmiCharactersSheetRecord:
        result = LakshmiCharactersSheetRecord()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.__sheet_controller.find_character_by_unique_id(author_id, unique_id)
        if len(df) == 0:
            # 登録がない
            raise LakshmiErrors.CharacterNotFoundException()

        result.set_values(
            df["unique_id"].values[0],
            df["site_id1"].values[0],
            df["site_id2"].values[0],
            df["site_url"].values[0],
            df["character_name"].values[0],
            df["character_image_url"].values[0],
            author_id,
            author_name,
            df["active"].values[0],
            df["lost"].values[0],
        )

        index = int(df.index[0])
        self.__sheet_controller.delete_character_by_index(index)

        # NOTE: self.__sheet_controllerのfind等からsaveまでの間にawait処理が入らないように注意。
        await self.background_save()
        return result

    async def character_list(self, context: commands.Context) -> List[LakshmiCharactersSheetRecord]:
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
                    row["lost"],
                )
                result.append(record)
        return result

    async def character_change(self, context: commands.Context, unique_id: str) -> LakshmiCharactersSheetRecord:
        result = LakshmiCharactersSheetRecord()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.__sheet_controller.find_character_by_unique_id(author_id, unique_id)
        if len(df) == 0:
            # 登録がない
            raise LakshmiErrors.CharacterNotFoundException()

        self.__sheet_controller.set_inactive_all_character_by_author_id(author_id)

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
            df["lost"].values[0],
        )
        self.__sheet_controller.update_character_by_index(index, result)

        # NOTE: self.__sheet_controllerのfind等からsaveまでの間にawait処理が入らないように注意。
        await self.background_save()
        return result

    async def set_image(self, context: commands.Context, unique_id: str, image_url: str) -> LakshmiCharactersSheetRecord:
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
            df["lost"].values[0],
        )
        self.__sheet_controller.update_character_by_index(index, result)

        # NOTE: self.__sheet_controllerのfind等からsaveまでの間にawait処理が入らないように注意。
        await self.background_save()
        return result

    async def set_lost(self, context: commands.Context, unique_id: str) -> LakshmiCharactersSheetRecord:
        result = LakshmiCharactersSheetRecord()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.__sheet_controller.find_character_by_unique_id(author_id, unique_id)
        if len(df) == 0:
            # 登録がない
            raise LakshmiErrors.CharacterNotFoundException()

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
            df["active"].values[0],
            True,
        )
        self.__sheet_controller.update_character_by_index(index, result)

        # NOTE: self.__sheet_controllerのfind等からsaveまでの間にawait処理が入らないように注意。
        await self.background_save()
        return result

    async def info_information(self, context: commands.Context, unique_id: str) -> Investigator:
        result = Investigator()

        author_id = str(context.author.id)
        author_name = str(context.author.name)

        df = self.__sheet_controller.find_character_by_unique_id(author_id, unique_id)
        if len(df) == 0:
            # 登録がない
            raise LakshmiErrors.CharacterNotFoundException()

        # 登録済み
        record = LakshmiCharactersSheetRecord()
        record.set_values(
            df["unique_id"].values[0],
            df["site_id1"].values[0],
            df["site_id2"].values[0],
            df["site_url"].values[0],
            df["character_name"].values[0],
            df["character_image_url"].values[0],
            author_id,
            author_name,
            df["active"].values[0],
            df["lost"].values[0],
        )
        self.set_investigator_by_record(result, record)

        #NOTE: find_character_by_unique_idの後だが、background_saveしないのでOKとする。
        if not await self.request(result, record.site_url):
            # TODO: delete sheet char
            raise LakshmiErrors.CharacterNotFoundException()

        return result

    def set_investigator_by_record(self, target: Investigator, record: LakshmiCharactersSheetRecord):
        target.unique_id = str(record.unique_id)
        target.site_id1 = str(record.site_id1)
        target.site_id2 = str(record.site_id2)
        target.site_url = str(record.site_url)
        target.personal_data.name = str(record.character_name)
        target.image_url = str(record.character_image_url)
        target.author_id = str(record.author_id)
        target.author_name = str(record.author_name)
        target.active = bool(record.active)
        target.lost = bool(record.lost)
        return self
