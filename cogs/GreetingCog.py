#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import math
import random

import nagisa

import discord
from discord.ext import commands

class GreetingCog(commands.Cog, name='挨拶系'):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.command()
    async def nagisa(self, context, *, message):
        """指定した文章を形態素解析します。"""
        result = "お望みの **形態素解析結果** よ。\n"
        words = nagisa.tagging(message)
        for index in range(len(words.words)):
            word = words.words[index]
            postag = words.postags[index]
            result += " " + word + "`[" + postag + "]`"
        await context.send(result)

    @commands.command()
    async def hello(self, context):
        """簡単な応答を返します。(Lakshmiの生存確認用)"""
        await context.send('やっほー')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            # メンションで話しかけられた
            if self.bot.user in message.mentions:
                character_message = self.bot.storage.get_character_message_when_talked_to_by_mention()
                await message.channel.send(f'{message.author.mention} {character_message}')

            # 挨拶メッセージを見つけた
            if self.bot.storage.is_say_hello(message):
                character_message = self.bot.storage.get_character_message_for_greeting_text(message)
                await message.channel.send(f'{character_message}')

def setup(bot):
    bot.add_cog(GreetingCog(bot))
