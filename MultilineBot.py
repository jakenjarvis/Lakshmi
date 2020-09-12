#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import List, Dict

import mojimoji

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

        self.__last_original_content = None

    @property
    def last_original_content(self):
        return self.__last_original_content

    # override
    async def process_commands(self, message):
        if message.author.bot:
            return

        # Backup original content
        self.__last_original_content = message.content
        print("--Original message:\n" + self.__last_original_content)

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
                    await self.invoke(ctx)
        else:
            # 通常時は本来通り動作させる。
            ctx = await self.get_context(message)
            await self.invoke(ctx)
