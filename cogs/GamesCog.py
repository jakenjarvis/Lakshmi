#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

from contents.games.GameHighAndLow import GameHighAndLow
import LakshmiErrors

class GamesCog(commands.Cog, name='ゲーム系'):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.group()
    async def game(self, context: commands.Context):
        """詳細は ;help game で確認してください。"""
        if context.invoked_subcommand is None:
            raise LakshmiErrors.SubcommandNotFoundException()

    @game.command(aliases=['highlow','hl'])
    async def highandlow(self, context: commands.Context):
        """ゲーム「High and Low」でLakshmiと遊びます。"""
        await self.bot.change_presence(activity=discord.Game(name='High and Low'))
        game = GameHighAndLow(self.bot)
        await game.high_and_low(context)
        await self.bot.change_presence(activity=None)

def setup(bot):
    bot.add_cog(GamesCog(bot))
