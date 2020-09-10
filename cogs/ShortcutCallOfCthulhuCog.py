#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import asyncio

import LakshmiErrors
from contents.character.InvestigatorEmbedCreator import InvestigatorEmbedCreator
from contents.character.CharacterManager import CharacterManager
from contents.character.Investigator import Investigator

from cogs.CallOfCthulhuCog import CallOfCthulhuCog

class ShortcutCallOfCthulhuCog(commands.Cog, name='CoC-TRPG系Shortcut'):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

        # for test
        self.coccog: CallOfCthulhuCog = self.bot.get_cog("CoC-TRPG系") # 'cogs.CallOfCthulhuCog'
        print("for test")
        print("----------")
        print([command.name for command in self.coccog.get_commands()])
        print("----------")
        print([command.qualified_name for command in self.coccog.walk_commands()])
        print("----------")
        for name, func in self.coccog.get_listeners():
            print(name, '->', func)
        print("----------")

    @commands.command()
    async def cca(self, context: commands.Context, url: str):
        """Shortcut: ;coc character add"""
        await self.coccog.character_add(context, url)

    @commands.command()
    async def ccl(self, context: commands.Context):
        """Shortcut: ;coc character list"""
        await self.coccog.character_list(context)

    @commands.command()
    async def ccu(self, context: commands.Context):
        """Shortcut: ;coc character urls"""
        await self.coccog.character_urls(context)

    @commands.command()
    async def ccc(self, context: commands.Context):
        """Shortcut: ;coc character choice"""
        await self.coccog.character_choice(context)

    @commands.command()
    async def ccsi(self, context: commands.Context, unique_id: str, image_url: str):
        """Shortcut: ;coc character set image"""
        await self.coccog.set_image(context, unique_id, image_url)

    @commands.command()
    async def ccsc(self, context: commands.Context, unique_id: str):
        """Shortcut: ;coc character set change"""
        await self.coccog.set_change(context, unique_id)

    @commands.command()
    async def ccif(self, context: commands.Context, unique_id: str = ""):
        """Shortcut: ;coc character info full"""
        await self.coccog.info_full(context, unique_id)

    @commands.command()
    async def ccis(self, context: commands.Context, unique_id: str = ""):
        """Shortcut: ;coc character info short"""
        await self.coccog.info_short(context, unique_id)

    @commands.command()
    async def ccib(self, context: commands.Context, unique_id: str = ""):
        """Shortcut: ;coc character info backstory"""
        await self.coccog.info_backstory(context, unique_id)

def setup(bot):
    bot.add_cog(ShortcutCallOfCthulhuCog(bot))
