#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Callable

import asyncio

import discord
from discord.ext import commands, tasks

class ChoiceReactionFlow():
    def __init__(self, bot: commands.Bot, context: commands.Context):
        self.bot: commands.Bot = bot
        self.context: commands.Context = context
        self.bot_message: discord.Message = None
        self.used_emojis: List[str] = None
        self.index: int = 0

    def set_target_message(self, bot_message: discord.Message, used_emojis: List[str]):
        self.bot_message = bot_message
        self.used_emojis = used_emojis
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

        choice_emoji = None
        try:
            #print(f"wait_for: start")
            reaction, member = await self.bot.wait_for(
                'reaction_add', check=check, timeout=timeout
            )
            #print(f"wait_for: end")
            choice_emoji = reaction.emoji
        except asyncio.TimeoutError:
            choice_emoji = None

        if cancel:
            #print(f"reaction_appender: cancel")
            self.reaction_appender.cancel()

        #print(f"choice_emoji: {choice_emoji}")
        return choice_emoji

    @tasks.loop()
    async def reaction_appender(self):
        #print(f"reaction_appender: {self.index}")
        emoji = self.used_emojis[self.index]
        await self.bot_message.add_reaction(emoji)
        self.index += 1
