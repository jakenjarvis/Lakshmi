#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

from LakshmiErrors import CharacterNotFoundException

from contents.CharacterGetter import CharacterGetter
from contents.InvestigatorEmbedCreator import InvestigatorEmbedCreator

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

            getter = CharacterGetter()
            character = getter.request(url)
            if character:
                print(character.name)
                #result = f'{context.author.mention} {character.name} {character.age} {character.sex} {character.occupation}\n{character.memo}'
                #await context.send(result)
                embed = InvestigatorEmbedCreator.create(character)
                await context.send(embed=embed)
            else:
                raise CharacterNotFoundException()

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

def setup(bot):
    bot.add_cog(CallOfCthulhuCog(bot))
