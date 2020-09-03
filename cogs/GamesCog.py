#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

from contents.GameHighAndLow import GameHighAndLow
from LakshmiErrors import SubcommandNotFoundException

class GamesCog(commands.Cog, name='ゲーム系'):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.group()
    async def game(self, context):
        if context.invoked_subcommand is None:
            raise SubcommandNotFoundException()

    @game.command(aliases=['highandlow','highlow','hl'])
    async def highandlow(self, context):
        """ゲーム「High and Low」でLakshmiと遊びます。"""
        game = GameHighAndLow(self.bot)
        game.high_and_low(context)

def setup(bot):
    bot.add_cog(GamesCog(bot))
