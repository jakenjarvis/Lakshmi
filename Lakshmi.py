#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
import traceback

import discord
from discord.ext import commands

from MultilineBot import MultilineBot
from LakshmiStorage import LakshmiStorage
from LakshmiErrors import PermissionNotFoundException, ArgumentOutOfRangeException

bot = MultilineBot(command_prefix=':')
bot.storage = LakshmiStorage()


extensions = [
    'cogs.DiceBotCog',
]
for extension in extensions:
    bot.load_extension(extension)

# NOTE: キャラ設定：セリフ少な目で、おとなしい感じの、点々多めで、言い切りタイプ。
#       柔らかいイメージ。林檎好き。
#       一人称は「私」、相手の呼び方は「あなた」、語尾が「～ね」
# --------------------------------------------------------------------------------
#　…あ　　はっきり気付いた感じ
#　…ん　　気付いているがあまり驚いてはいない様子
#　…お　　珍しいものをみた気付き方
#　…むぅ　気付いて少し怒っている様子
#　…え？　呆気にとられた気付き方
#　…ひぃ　怖いものを見て驚きながらも気付いた様子
# --------------------------------------------------------------------------------
character_command_not_found_dialogue = [
    "…ん。入力ミスを感知。私、アップルパイを焼いてるところだから、あなたが直しておいてね。",
    "…むぅ。入力ミスを感知。でも…私、もう限界…。あとはあなたに任せた…。( ˘ω˘)ｽﾔｧ……あっ、いけない…寝てた…。",
    "…あ。入力ミスを感知。…あれ、目を離した隙に私の林檎が（ｷｮﾛｷｮﾛ)。私が林檎を探している間に直しておいて。…さて、林檎林檎（ｷｮﾛｷｮﾛ）",
    "…お。入力ミスを感知。そんなことより、きょ…今日から深夜アニメに挑戦よ…。あなたが入力ミスを直している間に、全話見てあげるからね。",
    "…あ。入力ミスを感知。それよりもこのクマのぬいぐるみ…これは買いね……。私がこれを買う間に入力ミスを直しておいてね。あぁ…、このクマ最高……( ˘ω˘)♡",
    "あなたの文字が何かわからなかったせいで、今、私はヨガみたいなポーズをとらされているわ……ダイスなんて振れない！",
    "…ひっ…入力ミスがあるわ…。私は『くとぅるふ』の 『るーるぶっく』を読んでるから…貴方は入力ミスを直しておいて。…私も探索してみたいな…。",
    "…ん。入力ミスを感知。(ﾓｸﾞﾓｸﾞ)焼きリンゴも案外悪くないわね……あつ…。あなたも入力ミスを直し終わったら食べさせてあげるからね。",
    #"…今のは何だろう…？　私がファンブル連発したら『おはシュミ』と、いわれるのかしら…。私がファンブルの具現化なんて…やだ…。",
    "…ん。入力ミスがあったみたい。私が読める字で書き直してね？",
    "…むぅ。貴方の入力ミスのせいで、処理ができなかった。…どう責任取ってくれるの？",
    "(ﾓｸﾞﾓｸﾞ)…林檎に夢中で、処理工程を見ていなかったけど…。入力ミスをしているわね。ちゃんと確認してみて。",
]

@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions: # 話しかけられたかの判定
        await message.channel.send(f'{message.author.mention} ……ん？私を………呼んだ？')

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
