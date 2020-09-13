#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from discord.ext import commands

import LakshmiErrors
import MultilineBot
from contents.dice.DiceCommandProcessor import InvalidFormulaException, ArgumentOutOfRangeException, InvalidCharacterException
from contents.dice.CallOfCthulhuDice import CallOfCthulhuDice

class DiceBotCog(commands.Cog, name='ダイス系'):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.command()
    async def p(self, context: commands.Context, *, command: str):
        """1d100固定のパーセント指定でダイスを振ります。(percent)"""
        stock = []
        stock.append(f'{context.author.mention}')

        result = ""
        try:
            result = CallOfCthulhuDice().percent(command)
        except InvalidFormulaException as e:
            raise commands.CommandNotFound
        except ArgumentOutOfRangeException as e:
            raise LakshmiErrors.ArgumentOutOfRangeException
        except InvalidCharacterException as e:
            raise commands.CommandNotFound

        stock.append(f'{result}')
        await self.bot.send("\n".join(stock))

    @commands.command()
    async def vs(self, context: commands.Context, *, command: str):
        """対抗ロールでダイスを振ります。(versus)"""
        stock = []
        stock.append(f'{context.author.mention}')

        result = ""
        try:
            result = CallOfCthulhuDice().versus(command)
        except InvalidFormulaException as e:
            raise commands.CommandNotFound
        except ArgumentOutOfRangeException as e:
            raise LakshmiErrors.ArgumentOutOfRangeException
        except InvalidCharacterException as e:
            raise commands.CommandNotFound

        stock.append(f'{result}')
        await self.bot.send("\n".join(stock))

    @commands.command()
    async def f(self, context: commands.Context, *, command: str):
        """mDn形式で面を指定してダイスを振ります。(fate)"""
        stock = []
        stock.append(f'{context.author.mention}')

        result = ""
        try:
            result = CallOfCthulhuDice().roll(command)
        except InvalidFormulaException as e:
            raise commands.CommandNotFound
        except ArgumentOutOfRangeException as e:
            raise LakshmiErrors.ArgumentOutOfRangeException
        except InvalidCharacterException as e:
            raise commands.CommandNotFound

        stock.append(f'{result}')
        await self.bot.send("\n".join(stock))

    @commands.command()
    async def sf(self, context: commands.Context, *, command: str):
        """fと同じ。結果をDMで通知します。(secret fate)"""
        stock = []
        # メッセージの組み立て NOTE: DMするのでメンションは付けない
        #stock.append(f'{context.author.mention}')
        result = ""
        try:
            result = CallOfCthulhuDice().roll(command)
        except InvalidFormulaException as e:
            raise commands.CommandNotFound
        except ArgumentOutOfRangeException as e:
            raise LakshmiErrors.ArgumentOutOfRangeException
        except InvalidCharacterException as e:
            raise commands.CommandNotFound

        stock.append(f'{result}')
        await self.bot.author.send("\n".join(stock))

def setup(bot):
    bot.add_cog(DiceBotCog(bot))
