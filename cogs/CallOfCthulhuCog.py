#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

from LakshmiErrors import CharacterNotFoundException

from contents.CharacterVampireBloodNetGetter import CharacterVampireBloodNetGetter

class CallOfCthulhuCog(commands.Cog, name='CoC-TRPG系'):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.command()
    async def request(self, context: commands.Context, url: str):
        """テスト"""
        try:
            result = ""
            await context.trigger_typing()

            getter = CharacterVampireBloodNetGetter()
            character = getter.request(url)
            if character:
                print(character.name)
                result = f'{context.author.mention} {character.name} {character.age} {character.sex} {character.occupation}\n{character.memo}'
                await context.send(result)
            else:
                raise CharacterNotFoundException()

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

def setup(bot):
    bot.add_cog(CallOfCthulhuCog(bot))
