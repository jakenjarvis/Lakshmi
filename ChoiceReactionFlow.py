#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Callable
from collections import OrderedDict
import itertools
import asyncio

import discord
from discord.ext import commands, tasks

class ChoiceReactionFlowException(Exception):
    pass

class ArgumentOutOfRangeException(ChoiceReactionFlowException):
    pass

class ChoiceReactionFlow():
    # Discord API Max 20
    CHOICE_EMOJIS = itertools.cycle([
        "0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣",
        "♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓", # 12 Zodiac Emoji
        ])

    def __init__(self, bot: commands.Bot, context: commands.Context):
        self.bot: commands.Bot = bot
        self.context: commands.Context = context
        self.bot_message: discord.Message = None

        self.datastore: OrderedDict[str, Dict[str, any]] = {}
        self.used_emojis: List[str] = []

        self.index: int = 0

        self.choice_emoji = None

    def pick_next_emojis(self) -> str:
        return next(ChoiceReactionFlow.CHOICE_EMOJIS)

    def append_datastore(self, emoji, keyword="", **kwargs):
        if len(self.used_emojis) >= 20:
            raise ArgumentOutOfRangeException

        kwargs["key"] = str(keyword if len(keyword) >= 1 else emoji)
        kwargs["emoji"] = emoji
        kwargs["keyword"] = keyword
        # Duplicate check
        self.datastore[kwargs["key"]] = kwargs
        self.used_emojis.append(emoji)
        return self

    def get_chosed_datastore(self) -> Dict[str, any]:
        chosed_index = self.get_chosed_emoji_index()
        return list(self.datastore.items())[chosed_index][1]

    def get_chosed_emoji_index(self) -> int:
        return self.used_emojis.index(self.choice_emoji)

    def set_target_message(self, bot_message: discord.Message):
        self.bot_message = bot_message
        return self

    def check_choice_reaction_by_author_only(self) -> Callable[[discord.Reaction, discord.Member], bool]:
        return lambda reaction, member: all([
            member.id == self.context.author.id,
            reaction.emoji in self.used_emojis,
            reaction.message.id == self.bot_message.id
        ])

    async def wait_for_choice_reaction(self, *, check: Callable[[discord.Reaction, discord.Member], bool]=None, timeout: int=None, cancel: bool=True) -> str:
        if not check:
            check = self.check_choice_reaction_by_author_only()

        # ここでadd_reactionを実行すると、Emojiの数が多い場合にwait_forで待ち受けする前に
        # ユーザの入力が終わってしまうケースがあります。
        # これではユーザの入力を取りこぼす為、ユーザビリティが非常に悪くなります。
        # 遅延が発生しますが、wait_forで待機している間にadd_reactionで追加することで、
        # botがユーザの入力を見逃さなくなります。
        # If add_reaction is executed here, the user input may end before waiting with
        #  wait_for when the number of Emoji is large.
        # This will miss the user's input, which will greatly reduce usability.
        # There will be a delay, but by adding it with add_reaction while waiting with
        #  wait_for, the bot will not miss the user's input.
        self.index = 0
        self.reaction_appender.count = len(self.used_emojis)
        #print(f"reaction_appender: start")
        self.reaction_appender.start()

        try:
            #print(f"wait_for: start")
            reaction, member = await self.bot.wait_for(
                'reaction_add', check=check, timeout=timeout
            )
            #print(f"wait_for: end")
            self.choice_emoji = reaction.emoji
        except asyncio.TimeoutError:
            self.choice_emoji = None

        if cancel:
            #print(f"reaction_appender: cancel")
            self.reaction_appender.cancel()

        #print(f"choice_emoji: {choice_emoji}")
        return self.choice_emoji

    @tasks.loop()
    async def reaction_appender(self):
        #print(f"reaction_appender: {self.index}")
        emoji = self.used_emojis[self.index]
        await self.bot_message.add_reaction(emoji)
        self.index += 1
