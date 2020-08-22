#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import random
import math

class LakshmiStorage():
    def __init__(self):
        pass








"""

@client.event
async def on_ready():
    pass

@client.event
async def on_message(message):

    #print(str(message.content).splitlines())

    if message.author == client.user:
        return

    if client.user in message.mentions: # 話しかけられたかの判定
        await send_reply(message, "ん？わたくしを呼びました？")

    if message.content.startswith('/hello'):
        await message.channel.send('こんにちは！わたくしに何か御用ですか？')

    if message.content.startswith('/cf'):
        check = VALID_CHARACTERS.match(str(message.content))
        if check:
            match = VALID_DICE.search(str(message.content))
            if match:
                command = str(match.group(1)).lower()
                number = int(match.group(2))
                surface = int(match.group(3))

                total = 0
                rolls = []
                for _ in range(number):
                    value = random.randint(1, surface)
                    rolls.append(str(value))
                    total += value
                roll = "+".join(rolls)

                await send_reply(message, f"{command} = ({roll}) = {str(total)}")

            else:
                await send_message(message, 'ちょっと何を言っているのか、わからないわ！(A)')
        else:
            await send_message(message, 'ちょっと何を言っているのか、わからないわ！(B)')

@client.event
async def on_reaction_add(reaction, user):
    pass

async def send_message(message, text):
    await message.channel.send(text)

async def send_reply(message, text):
    reply = f'{message.author.mention} {text}'
    await message.channel.send(reply)

client.run(token)


"""
