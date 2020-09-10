#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

import datetime
import asyncio
import nagisa

import discord
from discord.ext import commands

class GreetingCog(commands.Cog, name='挨拶系'):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.command()
    async def nagisa(self, context: commands.Context, *, message: str):
        """指定した文章を形態素解析します。"""
        try:
            character_message = self.bot.storage.lexicon.get_character_message_for_command_nagisa()
            result = f"{character_message}\n"

            await context.trigger_typing()

            words = nagisa.tagging(message)
            for index in range(len(words.words)):
                word = words.words[index]
                postag = words.postags[index]
                result += " " + word + "`[" + postag + "]`"

            await context.send(result)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @commands.command()
    async def hello(self, context: commands.Context):
        """簡単な応答を返します。(Lakshmiの生存確認用)"""
        try:
            character_message = self.bot.storage.lexicon.get_character_message_for_command_hello()
            await context.send(character_message)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author != self.bot.user:
            # メンションで話しかけられた
            if self.bot.user in message.mentions:
                character_message = self.bot.storage.lexicon.get_character_message_when_talked_to_by_mention()
                await message.channel.send(f'{message.author.mention} {character_message}')

            # 挨拶メッセージを見つけた
            if self.bot.storage.lexicon.is_say_hello(message):
                await message.channel.trigger_typing()
                await asyncio.sleep(4) # わざとちょっと遅れて反応する
                character_message = self.bot.storage.lexicon.get_character_message_for_greeting_text(message)
                await message.channel.send(f'{character_message}')

    @commands.Cog.listener()
    async def on_typing(self, channel: discord.abc.Messageable, user: Union[discord.User, discord.Member], when: datetime.datetime):
        # 誰かがメッセージを入力し始めたときに呼び出されます。
        # https://discordpy.readthedocs.io/ja/latest/api.html#discord.on_typing
        # channel == discord.TextChannel  : user == discord.Member
        # channel == discord.GroupChannel : user == discord.User
        # channel == discord.DMChannel    : user == discord.User
        pass

def setup(bot):
    bot.add_cog(GreetingCog(bot))
