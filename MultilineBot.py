#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import List, Dict, Tuple

import mojimoji

import discord
from discord.ext import commands

class MultilineBot(commands.Bot):
    def __init__(self, command_prefix, help_command=None, description=None, **options):
        # The default value of help_command cannot refer to the definition.
        if help_command:
            super().__init__(command_prefix, help_command, description, **options)
        else:
            super().__init__(command_prefix, description=description, **options)

        # self.command_prefix
        self.zenkaku_command_prefix = mojimoji.han_to_zen(self.command_prefix)

        regex_command_conditions = r"([" + self.command_prefix + self.zenkaku_command_prefix + r"]{1}[_0-9a-zA-Z＿０-９ａ-ｚＡ-Ｚ]+)"
        self.regex_command = re.compile(regex_command_conditions)

        self.__message_stocker: MessageAccumulation = None

    # override
    async def process_commands(self, message):
        if message.author.bot:
            return

        # Backup original content
        # その都度インスタンスを生成することにする。
        self.__message_stocker = MessageAccumulation(self, message)

        # 書き換え
        if message.content.startswith(self.command_prefix):
            # 先頭がcommand_prefixの時のみ改変処理を行う。
            # コマンド処理に差支えが無い範囲で、文字列加工を行う事。

            # コマンド相当文字の全角半角変換
            zen_to_han_command_line = self.regex_command.sub(
                lambda match: mojimoji.zen_to_han(match.group(0)).lower(),
                message.content)

            # 改行をマークしておき、一旦１行に纏めて、コマンドでsplitする。
            linking_command = ("🃴".join(zen_to_han_command_line.splitlines())).replace('　',' ')
            split_linking_command = self.regex_command.split(linking_command)
            removal_blank_line = [item for item in split_linking_command if item != ""]
            #print(f"removal_blank_line: {removal_blank_line}")

            # コマンド記号を先頭に内容を再組立てする。
            command_line_list = []
            split_line = []
            for item in removal_blank_line:
                if self.regex_command.match(item):
                    if len(split_line) >= 1:
                        command_line_list.append("".join(split_line))
                    split_line = []
                split_line.append(item)
            if len(split_line) >= 1:
                command_line_list.append("".join(split_line))
            #print(f"command_line_list: {command_line_list}")

            # message.contentを改変し、通常処理のように偽装する。
            for command_line in command_line_list:
                cr_lines = [item for item in command_line.replace('🃴', '\n').splitlines() if item != ""]
                for line in cr_lines:
                    # new message.content
                    message.content = line
                    print("----Modified message:\n" + message.content)

                    # NOTE: この時、message.deleteを使い、
                    # コマンドを打ったユーザーのメッセージを削除するような処理を行うと、
                    # 一つのメッセージに対し、２回の削除が走ってしまう可能性があるため注意。
                    ctx = await self.get_context(message)
                    self.__message_stocker.set_last_context(ctx)
                    await self.invoke(ctx)

            # ストックしたメッセージを一気に送信する。
            await self.__message_stocker.release_send()

        else:
            # 通常時は本来通り動作させる。
            ctx = await self.get_context(message)
            self.__message_stocker.set_last_context(ctx)
            await self.invoke(ctx)

    @property
    def author(self):
        self.__message_stocker.set_target_id(self.__message_stocker.context.author.id)
        return self.__message_stocker

    async def send(self, content=None, *, tts=False, embed=None, file=None,
                                          files=None, delete_after=None, nonce=None,
                                          allowed_mentions=None):
        self.__message_stocker.set_target_id(self.__message_stocker.context.channel.id)
        return await self.__message_stocker.stock_send(content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce, allowed_mentions=allowed_mentions)


class MessageAccumulation():
    def __init__(self, bot: MultilineBot, message: discord.Message):
        self.bot = bot
        self.message = message

        self.stock: Dict[int, List[Tuple[any, any]]] = {}

        self.__original_content = message.content
        print("--Original message:\n" + self.__original_content)

        self.__last_context: commands.Context = None
        self.__last_send_target_id: int = 0

    @property
    def original_content(self):
        return self.__original_content

    @property
    def context(self) -> commands.Context:
        return self.__last_context

    def set_last_context(self, context: commands.Context):
        self.__last_context = context

    def set_target_id(self, id: int):
        self.__last_send_target_id = id
        if not self.__last_send_target_id in self.stock:
            self.stock[self.__last_send_target_id] = []

    async def send(self, content=None, *, tts=False, embed=None, file=None,
                                          files=None, delete_after=None, nonce=None,
                                          allowed_mentions=None):
        await self.stock_send(content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce, allowed_mentions=allowed_mentions)

    async def stock_send(self, *args, **kwargs):
        #print("stock_send")
        self.stock[self.__last_send_target_id].append((args, kwargs))

    async def release_send(self):
        #print("release_send")
        for id in self.stock.keys():
            texts = []
            for params in self.stock[id]:
                args = params[0]
                kwargs = params[1]
                #print(f"params = args: {args}, kwargs: {kwargs}")

                if self.is_send_kwargs(kwargs):
                    # テキスト以外の送信分は、個別にSendする。
                    if len(texts) >= 1:
                        # ストックメッセージがあるなら送信する。
                        await self.__send_join(id, texts)
                        texts = []
                    # メッセージ送信
                    await self.__send(id, *args, **kwargs)

                else:
                    if len(args) >= 1:
                        texts.append(args[0])

            if len(texts) >= 1:
                # ストックメッセージがあるなら送信する。
                await self.__send_join(id, texts)
                texts = []

    def is_send_kwargs(self, kwargs: Dict[str, any]):
        return not all([
            kwargs['tts'] == False,
            kwargs['embed'] is None,
            kwargs['file'] is None,
            kwargs['files'] is None,
            kwargs['delete_after'] is None,
            kwargs['nonce'] is None,
            kwargs['allowed_mentions'] is None
        ])

    async def __send_join(self, id: int, texts: List[str]):
        #print("__send_join")
        # TODO: 意図的に実行するケースとしないケースを分けたい。
        # TODO: 消費したメッセージをPOPとかして取り出さないと２重送信してしまう。
        message = "🃴".join("🃴".join(texts).splitlines())
        if f'{self.context.author.mention}' in message:
            message = f"{self.context.author.mention}🃴{message.replace(f'{self.context.author.mention}','')}"
        message = '\n'.join([item for item in message.replace('🃴', '\n').splitlines() if item != ""])
        await self.__send(id, message)

    async def __send(self, id: int, *args, **kwargs):
        #print("__send")
        # TODO:
        if id == self.context.channel.id:
            await self.context.send(*args, **kwargs)

        elif id == self.context.author.id:
            await self.context.author.send(*args, **kwargs)
