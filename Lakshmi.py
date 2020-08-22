#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
import os
import traceback
from aiohttp import connector

token = ""
try:
    # Heroku環境
    token = os.environ['DISCORD_TOKEN']
except Exception as e:
    # ローカル環境
    with open(r"token.txt", "r", encoding="utf-8") as file:
        token = file.read()

client = discord.Client()

@client.event
async def on_ready():
    print('ログインしました！わたくし、楽 朱美 がダイス結果をお伝えします！よろしくね～！')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/hello'):
        await message.channel.send('こんにちは！わたくしに何か御用ですか？')

client.run(token)
