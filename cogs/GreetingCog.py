#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import math
import random

from discord.ext import commands

class GreetingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.command()
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
            if self.bot.storage.is_say_hello(message.content):
                character_message = self.bot.storage.get_character_message_for_greeting_text(message.author.display_name)

def setup(bot):
    bot.add_cog(GreetingCog(bot))
