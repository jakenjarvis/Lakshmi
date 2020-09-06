#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

from contents.character.InvestigatorEmbedCreator import InvestigatorEmbedCreator
from LakshmiErrors import SubcommandNotFoundException
from contents.character.CharacterManager import CharacterManager
from contents.character.Investigator import Investigator

# TODO:
# :coc character add <URL> キャラ登録でスプレッドシート記録
# :coc character delete <キャラID> キャラ登録情報削除
# :coc character list 登録済みキャラの一覧表示
# :coc character change <キャラID|active> 使用中キャラの設定
# :coc character set image <キャラID|active> <画像URL> で、キャラ画像URLの登録
# :coc character info full <キャラID|active>  キャラのステータス表示（フル）
# :coc character info short <キャラID|active>  キャラのステータス表示（簡易）
# :coc character info backstory <キャラID|active>  キャラのステータス表示（キャラ紹介）

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

    @character.command(name='add', aliases=['a'])
    async def character_add(self, context: commands.Context, url: str):
        """ キャラクターシートのURLを指定してLakshmiに登録します。 """
        try:
            result = f""
            await context.trigger_typing()

            manager = CharacterManager(self.bot)
            character = manager.character_add(context, url)

            result += f"…ふぅ。無事……{character.character_name}さんを登録したわ……。\n"
            result += f"Idは {character.unique_id} よ…。"
            await context.send(result)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @character.command(name='list', aliases=['l'])
    async def character_list(self, context: commands.Context):
        """ Lakshmiに登録済みのキャラクターシートの一覧を表示します。 """
        try:
            result = f""

            author_name = str(context.author.name)
            display_name = str(context.author.display_name)

            await context.trigger_typing()

            manager = CharacterManager(self.bot)

            records = manager.character_list(context)
            if len(records) >= 1:
                result += f"…ん。あなたの登録キャラクターは次の{len(records)}人よ……。"
                result += f"\n"
                result += f"```"
                for record in records:
                    result += f"{record.to_display_string()}\n"
                result += f"```"
            else:
                result += f"あ……。あなたの登録キャラクターが見つからないわ………。"

            await context.send(result)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @character.group(aliases=['i'])
    async def info(self, context: commands.Context):
        """詳細は :help coc character info で確認してください。"""
        if context.invoked_subcommand is None:
            raise SubcommandNotFoundException()

    @info.command(name='full', aliases=['f'])
    async def info_full(self, context: commands.Context, unique_id: str):
        """ キャラクターシートのIDを指定して情報（Full）を表示します。 """
        try:
            await context.trigger_typing()

            manager = CharacterManager(self.bot)
            character = manager.info_full(context, unique_id)

            embed = InvestigatorEmbedCreator.create_full_status(character)
            await context.send(embed=embed)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

def setup(bot):
    bot.add_cog(CallOfCthulhuCog(bot))
