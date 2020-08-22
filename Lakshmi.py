import discord
import os
import traceback

token = os.environ['DISCORD_TOKEN']

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
