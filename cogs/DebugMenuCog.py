#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union
import asyncio

import discord
from discord.ext import commands, menus

import LakshmiErrors

class DebugMenuCog(commands.Cog, name='Debug開発系'):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.group(hidden=True)
    async def debug(self, context: commands.Context):
        if context.invoked_subcommand is None:
            raise LakshmiErrors.SubcommandNotFoundException()

    @debug.command()
    async def menu(self, context: commands.Context):
        menu = MyMenu()
        await menu.start(context)

    @debug.command()
    async def confirm(self, context: commands.Context):
        confirm = await Confirm('Delete everything?').prompt(context)
        if confirm:
            await context.send('deleted...')

    @debug.command()
    async def mysource(self, context: commands.Context):
        pages = menus.MenuPages(source=MySource(range(1, 100)), clear_reactions_after=True)
        await pages.start(context)

    @debug.command()
    async def groupby(self, context: commands.Context):
        pages = menus.MenuPages(source=GroupBySource(data, key=lambda t: t.key, per_page=12), clear_reactions_after=True)
        await pages.start(context)

    @debug.command()
    async def asynciter(self, context: commands.Context):
        pages = menus.MenuPages(source=AsyncIteratorSource(), clear_reactions_after=True)
        await pages.start(context)


# --------------------------------------------------
#
# --------------------------------------------------
class MyMenu(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        return await channel.send(f'Hello {ctx.author}')

    @menus.button('\N{THUMBS UP SIGN}')
    async def on_thumbs_up(self, payload):
        await self.message.edit(content=f'Thanks {self.ctx.author}!')

    @menus.button('\N{THUMBS DOWN SIGN}')
    async def on_thumbs_down(self, payload):
        await self.message.edit(content=f"That's not nice {self.ctx.author}...")

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        self.stop()


# --------------------------------------------------
#
# --------------------------------------------------
class Confirm(menus.Menu):
    def __init__(self, msg):
        super().__init__(timeout=30.0, delete_message_after=True)
        self.msg = msg
        self.result = None

    async def send_initial_message(self, ctx, channel):
        return await channel.send(self.msg)

    @menus.button('\N{WHITE HEAVY CHECK MARK}')
    async def do_confirm(self, payload):
        self.result = True
        self.stop()

    @menus.button('\N{CROSS MARK}')
    async def do_deny(self, payload):
        self.result = False
        self.stop()

    async def prompt(self, ctx):
        await self.start(ctx, wait=True)
        return self.result


# --------------------------------------------------
#
# --------------------------------------------------
class MySource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=4)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        return '\n'.join(f'{i}. {v}' for i, v in enumerate(entries, start=offset))


# --------------------------------------------------
#
# --------------------------------------------------
class Test:
    def __init__(self, key, value):
        self.key = key
        self.value = value

data = [
    Test(key=key, value=value)
    for key in ['test', 'other', 'okay']
    for value in range(20)
]

class GroupBySource(menus.GroupByPageSource):
    async def format_page(self, menu, entry):
        joined = '\n'.join(f'{i}. <Test value={v.value}>' for i, v in enumerate(entry.items, start=1))
        return f'**{entry.key}**\n{joined}\nPage {menu.current_page + 1}/{self.get_max_pages()}'


# --------------------------------------------------
#
# --------------------------------------------------
class Test2:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<Test value={self.value}>'

async def generate(number):
    for i in range(number):
        yield Test2(i)

class AsyncIteratorSource(menus.AsyncIteratorPageSource):
    def __init__(self):
        super().__init__(generate(9), per_page=4)

    async def format_page(self, menu, entries):
        start = menu.current_page * self.per_page
        return f'\n'.join(f'{i}. {v!r}' for i, v in enumerate(entries, start=start))



# --------------------------------------------------
#
# --------------------------------------------------
def setup(bot):
    bot.add_cog(DebugMenuCog(bot))
