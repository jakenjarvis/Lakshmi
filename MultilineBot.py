#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from collections import deque
from typing import List, Dict, Tuple, Deque, Union

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
        self.__message_stocker.set_target(self.__message_stocker.context.author)
        return self.__message_stocker

    async def send(self, content=None, *, tts=False, embed=None, file=None,
                                          files=None, delete_after=None, nonce=None,
                                          allowed_mentions=None):
        self.__message_stocker.set_target(self.__message_stocker.context.channel)
        return self.__message_stocker.append_queue(content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce, allowed_mentions=allowed_mentions)

class MessageAccumulation():
    def __init__(self, bot: MultilineBot, message: discord.Message):
        self.bot = bot
        self.message = message

        #self.stock: Dict[int, Deque[Tuple[any, any]]] = {}
        self.__queue: Deque[Tuple[any, str, any, any]] = deque([]) # target, mention, args, kwargs

        self.__original_content = message.content
        print("--Original message:\n" + self.__original_content)

        self.__last_context: commands.Context = None
        self.__last_send_target: Union[discord.TextChannel, discord.User] = None

    @property
    def original_content(self):
        return self.__original_content

    @property
    def context(self) -> commands.Context:
        return self.__last_context

    def set_last_context(self, context: commands.Context):
        self.__last_context = context

    def set_target(self, target: Union[discord.TextChannel, discord.User]):
        self.__last_send_target = target

    async def send(self, content=None, *, tts=False, embed=None, file=None,
                                          files=None, delete_after=None, nonce=None,
                                          allowed_mentions=None):
        self.append_queue(content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce, allowed_mentions=allowed_mentions)

    def append_queue(self, *args, **kwargs): # This is not async.
        #print("send_stock")
        mention = f'{self.__last_context.author.mention}'
        self.__queue.append((self.__last_send_target, mention, args, kwargs)) # target, mention, args, kwargs

    async def release_send(self):
        #print("release_send")

        to_be_send: Deque[Tuple[any, str, any, any]] = deque([]) # target, mention, args, kwargs
        texts = []

        last_status = (None, None)
        while 0 < len(self.__queue):
            params = self.__queue.popleft()
            target = params[0]
            mention = params[1]
            args = params[2]
            kwargs = params[3]
            #print(f"params = target: {target}, mention: {mention}, args: {args}, kwargs: {kwargs}")

            if self.is_send_kwargs(kwargs):
                # テキスト以外の送信分は、個別にSendする。
                #print(f"個別: {params}")
                to_be_send.append(params)
                last_status = (None, None)
            else:
                # テキストのみの送信の場合は、可能であれば集約する。
                content = str(args[0])
                if last_status != (target, mention):
                    #print(f"新規: {params}")
                    last_status = (target, mention)
                    texts = []
                    texts.append(content)
                    to_be_send.append(params)
                else:
                    #print(f"集約: {params}")
                    texts.append(content.replace(mention, "").strip()) # メンションを削除して追加
                    # 一旦取り出して再構築
                    last_params = to_be_send.pop()
                    to_be_send.append((last_params[0], last_params[1], ('\n'.join(texts),), last_params[3]))

        while 0 < len(to_be_send):
            # ストックメッセージがあるなら送信する。
            params = to_be_send.popleft()
            target = params[0]
            mention = params[1]
            args = params[2]
            kwargs = params[3]
            await self.__send(target.id, *args, **kwargs)

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

    async def __send(self, id: int, *args, **kwargs):
        #print("__send")
        # TODO:
        if id == self.context.channel.id:
            await self.context.send(*args, **kwargs)

        elif id == self.context.author.id:
            await self.context.author.send(*args, **kwargs)
