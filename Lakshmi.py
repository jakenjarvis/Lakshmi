#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
import traceback

import discord
from discord.ext import commands

from LakshmiStorage import LakshmiStorage
from LakshmiErrors import PermissionNotFoundException, ArgumentOutOfRangeException

bot = commands.Bot(command_prefix=':')
bot.storage = LakshmiStorage()


extensions = [
    'cogs.DiceBotCog',
]
for extension in extensions:
    bot.load_extension(extension)

# NOTE: キャラ設定：セリフ少な目で、おとなしい感じの、点々多めで、言い切りタイプ。一人称は「私」、語尾が「～ね」
character_command_not_found_dialogue = [
    "…？　今のは、なんだろう？　…ところで今、アップルパイを焼いてるの、おひとついかが？",
    "…？　( ˘ω˘)ｽﾔｧ…あっ、いけない…寝てた…。なんか今、言われた気がするけど…なんだろう…？",
    "…あれ、私の…林檎（ｷｮﾛｷｮﾛ）…何か言われた気がするけど…何だろう？　…それはさておき、林檎林檎（ｷｮﾛｷｮﾛ）",
    "…？　何か言われた気がするけど…？　きょ…今日から深夜アニメに挑戦よ…。…どれを見ようかすごく悩む…。",
    "あっ、このクマのぬいぐるみ…これは買いね……。今、何か言われた気がするけど…。あぁ…、このクマ最高……♡…( ˘ω˘)ｽﾔｧ",
    "何かわからなかったせいで、私は今、ヨガみたいなポーズをとらされているわ……ダイスなんて振れない！",
    "…今のは…？　今『くとぅるふ』の『るーるぶっく』を読んでるわ……。貴方達もやってる！？…私も探索したい…。",
    "…今のは何だろう…？　焼きリンゴも案外悪くないわね……あつ…。今度、貴方達にもおすそ分けしたい…。",
    "…今のは何だろう…？　私がファンブル連発したら『おはシュミ』と、いわれるのかしら…。私がファンブルの具現化なんて…やだ…。",
]

@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions: # 話しかけられたかの判定
        await message.channel.send(f'{message.author.mention} ……ん？私を………読んだ？')

@bot.event
async def on_command_error(context, error):
    # Throwしたいときは、以下のようにon_command_errorを呼び出す。
    # await self.bot.on_command_error(context, PermissionNotFound())

    if isinstance(error, ArgumentOutOfRangeException):
        await context.send(f'{context.author.mention} ごめんなさい……おっきくて、計算できないの……')

    elif isinstance(error, PermissionNotFoundException):
        await context.send(f'{context.author.mention} 貴方……権限が無いみたいよ………。')

    elif isinstance(error, commands.CommandNotFound):
        message = random.choice(character_command_not_found_dialogue)
        await context.send(f'{context.author.mention} {message}')

    else:
        original_error = getattr(error, "original", error)
        error_message = ''.join(traceback.TracebackException.from_exception(original_error).format())
        error_message = "```py\n" + error_message + "\n```"
        message = f'{context.author.mention}\n私の中で……何かが起こったようなの………。これを……開発者さんに知らせてあげて！\n{error_message}'
        await context.send(message)


token = ""
try:
    # Heroku環境
    token = os.environ['DISCORD_TOKEN']
except Exception as e:
    # ローカル環境
    with open(r"token.txt", "r", encoding="utf-8") as file:
        token = file.read()

bot.run(token)
