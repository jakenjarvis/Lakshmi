#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import mojimoji

from discord.ext import commands

class MultilineBot(commands.Bot):
    def __init__(self, command_prefix, help_command=None, description=None, **options):
        if help_command:
            super().__init__(command_prefix, help_command, description, **options)
        else:
            super().__init__(command_prefix, description=description, **options)

        # self.command_prefix
        self.zenkaku_command_prefix = mojimoji.han_to_zen(self.command_prefix)

        regex_command_conditions = r"([" + self.command_prefix + self.zenkaku_command_prefix + r"]{1}[_0-9a-zA-Z＿０-９ａ-ｚＡ-Ｚ]+)"
        self.regex_command = re.compile(regex_command_conditions)

        self.original_contents = {}

    # override
    async def process_commands(self, message):
        if message.author.bot:
            return

        print("---------- override process_commands() ----------")

        # Backup original content
        self.original_contents[message.id] = message.content
        print("-----original_contents:\n" + message.content)

        # 書き換え
        if message.content.startswith(self.command_prefix):
            # 先頭がcommand_prefixの時のみ改変処理を行う。
            # コメントがあるのでここでは.lower()しないこと。

            # コマンド相当文字の全角半角変換
            message.content = self.regex_command.sub(
                lambda match: mojimoji.zen_to_han(match.group(0)),
                message.content)

            # 改行をマークしておき、一旦１行に纏めて、コマンドでsplitする。
            linking_command = "🎲".join(message.content.splitlines())
            split_linking_command = self.regex_command.split(linking_command)
            removal_blank_items = [item for item in split_linking_command if item != ""]
            #print(removal_blank_items)

            # コマンド種類別に内容を再分配する。
            command_line_list = {}
            new_line = []
            key = ""
            for item in removal_blank_items:
                if self.regex_command.match(item):
                    item = item.lower()
                    key = item
                if not key in command_line_list.keys():
                    command_line_list[key] = []
                command_line_list[key].append(item)
            #print(command_line_list)

            # コマンド種類別にmessage.contentを改変し、通常処理のように偽装する。
            for key in command_line_list.keys():
                # new message.content
                print("-----key: " + key)
                message.content = ("".join(command_line_list[key])).replace('🎲', '\n')
                print("-----New message.content:\n" + message.content)

                # NOTE: この時、message.deleteを使い、
                # コマンドを打ったユーザーのメッセージを削除するような処理を行うと、
                # 一つのメッセージに対し、２回の削除が走ってしまう可能性があるため注意。
                ctx = await self.get_context(message)
                await self.invoke(ctx)
        else:
            # 通常時は本来通り動作させる。
            ctx = await self.get_context(message)
            await self.invoke(ctx)
