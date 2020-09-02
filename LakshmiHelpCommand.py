#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from discord.ext import commands

class LakshmiHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = "その他"
        self.command_attrs["help"] = "コマンド一覧と簡単な説明を表示"

    def get_ending_note(self):
        return (f"各コマンドの説明: {self.context.prefix}help <コマンド名>\n"
                f"各カテゴリの説明: {self.context.prefix}help <カテゴリ名>\n")
