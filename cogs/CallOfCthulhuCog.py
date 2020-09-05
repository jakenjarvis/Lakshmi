#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from distutils.util import strtobool

import discord
from discord.ext import commands

import ulid

from LakshmiErrors import SubcommandNotFoundException, CharacterNotFoundException
from contents.character.InvestigatorEmbedCreator import InvestigatorEmbedCreator
from contents.character.CharactersSheetController import CharactersSheetController
from contents.character.CharacterGetter import CharacterGetter
from contents.character.Investigator import Investigator

# TODO:
# :coc character add <URL> キャラ登録でスプレッドシート記録
# :coc character delete <キャラID> キャラ登録情報削除
# :coc character list 登録済みキャラの一覧表示
# :coc character set active <キャラID|active> 使用中キャラの設定
# :coc character set image <キャラID|active> <画像URL> で、キャラ画像URLの登録
# :coc character status full <キャラID|active>  キャラのステータス表示（フル）
# :coc character status short <キャラID|active>  キャラのステータス表示（簡易）
# :coc character status backstory <キャラID|active>  キャラのステータス表示（キャラ紹介）

class CallOfCthulhuCog(commands.Cog, name='CoC-TRPG系'):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.group(aliases=['c'])
    async def coc(self, context: commands.Context):
        """詳細は :help coc で確認してください。"""
        if context.invoked_subcommand is None:
            raise SubcommandNotFoundException()

    @coc.group(aliases=['char','c'])
    async def character(self, context: commands.Context):
        """詳細は :help coc character で確認してください。"""
        if context.invoked_subcommand is None:
            raise SubcommandNotFoundException()

    @character.command(aliases=['req','r'])
    async def request(self, context: commands.Context, url: str):
        """テスト"""
        try:
            await context.trigger_typing()

            author_id = str(context.author.id)
            author_name = str(context.author.name)

            controller = CharactersSheetController(self.bot.storage.pandasheet)
            controller.load()

            getter = CharacterGetter()
            character = Investigator() # 格納用キャラクターインスタンス作成

            if not getter.request(character, url):
                raise CharacterNotFoundException()

            df = controller.find_character_by_site_url(author_id, url)
            if len(df) == 0:
                # 新規
                character.unique_key = ulid.new()
                character.author_id = author_id
                character.author_name = author_name
                character.active = False
                #print("ZZZZ1: " + str(character.active))
            else:
                # 登録済み
                character.unique_key = str(df["unique_key"].values[0])
                character.author_id = author_id
                character.author_name = author_name
                character.active = strtobool(df["active"].values[0])
                #print("ZZZZ2: " + str(character.active))

            controller.merge_character_by_site_url(
                character.unique_key,
                character.site_url,
                character.author_id,
                character.author_name,
                character.active,
                character.name,
                character.image_url
                )
            controller.save()

            embed = InvestigatorEmbedCreator.create_full_status(character)
            await context.send(embed=embed)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

def setup(bot):
    bot.add_cog(CallOfCthulhuCog(bot))
