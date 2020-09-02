#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import math
import random

import nagisa

import discord
from discord.ext import commands

class GreetingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.command(description="指定した文章を形態素解析します。")
    async def nagisa(self, context, *, message):
        result = "お望みの **形態素解析結果** よ。\n"
        words = nagisa.tagging(message)
        for index in range(len(words.words)):
            word = words.words[index]
            postag = words.postags[index]
            result += " " + word + "`[" + postag + "]`"
        await context.send(result)

    @commands.command(description="簡単な応答を返します。(Lakshmiの生存確認)")
    async def hello(self, context):
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
