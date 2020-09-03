#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import math
import random
import asyncio

import discord
from discord.ext import commands

# https://qiita.com/Shirataki2/items/9bdc62548e7b24d3c803

class GameHighAndLow():
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    async def high_and_low(self, context):
        """ゲーム「High and Low」でLakshmiと遊びます。"""
        card1 = Card.choice()
        card2 = Card.choice()

        bot_message = await context.channel.send(
            f'…ん。あたしと勝負するの？\n'+
            f'1枚目: {card1}\n' +
            f'2枚目は、これより………大きい？: ⬆　小さい？: ⬇　同じ？: ↔\n' +
            f'どれだと……思う？ 制限時間は30秒だからね………。\n'
        )
        emojis = ('⬆', '⬇', '↔')

        for emoji in emojis:
            await bot_message.add_reaction(emoji)

        def check_reaction(reaction: discord.Reaction, member: discord.Member):
            return all([
                member.id == context.author.id,
                reaction.emoji in emojis,
                reaction.message.id == bot_message.id
            ])

        emoji = None
        try:
            reaction, member = await self.bot.wait_for(
                'reaction_add', check=check_reaction, timeout=30
            )
            emoji = reaction.emoji
        except asyncio.TimeoutError:
            emoji = None

        if emoji:
            # 正解判定
            if any([
                emoji == emojis[0] and card1 < card2,
                emoji == emojis[1] and card1 > card2,
                emoji == emojis[2] and card1 == card2
            ]):
                await context.channel.send(f'おめでとう………{context.author.display_name}さんの勝ちよ……。')
            else:
                await context.channel.send(f'……残念ね……ハズレよ…。')
        else:
            await context.channel.send(f'時間切れよ………{context.author.display_name}さんの意気地なし…。')

        await context.channel.send(f'2枚目は{card2}だったのよ……。')


class Card:
    nums = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, num):
        if not num in self.nums:
            raise ValueError
        self.num = num

    @classmethod
    def choice(cls):
        return cls(random.choice(cls.nums))

    def __str__(self):
        return self.num

    def __lt__(self, other):
        my_card = self.nums.index(self.num)
        other_card = self.nums.index(other.num)
        return my_card < other_card

    def __gt__(self, other):
        my_card = self.nums.index(self.num)
        other_card = self.nums.index(other.num)
        return my_card > other_card

    def __eq__(self, other):
        my_card = self.nums.index(self.num)
        other_card = self.nums.index(other.num)
        return my_card == other_card
