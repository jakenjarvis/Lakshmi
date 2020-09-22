#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict
from distutils.util import strtobool
import aiohttp
import asyncio

import discord
from discord.ext import commands, tasks

class NameGenerator():
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        #self.bot.storage

    async def generate_name(self, gender: str) -> str:
        result = None
        response = None
        data = None
        try:
            request_url = self.bot.storage.environment.get_person_name_api_url()
            params = {"gender": f"{gender}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(request_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
        except Exception as e:
            response = None

        if response:
            result = f'{data["kanji_name"]}({data["kana_name"]})'
        return result
