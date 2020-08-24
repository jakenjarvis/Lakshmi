#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from discord.ext import commands

class MultilineBot(commands.Bot):
    def __init__(self, command_prefix, help_command=None, description=None, **options):
        if help_command:
            super().__init__(command_prefix, help_command, description, **options)
        else:
            super().__init__(command_prefix, description=description, **options)

        self.__store_send_data = {}

    # override
    async def process_commands(self, message):
        if message.author.bot:
            return

        # TODO:
        ctx = await self.get_context(message)
        await self.invoke(ctx)

        # added event
        await self.on_after_process_commands()

    # added event
    async def on_after_process_commands(self):
        for target_context in self.__store_send_data.keys():
            for store in self.__store_send_data[target_context]:
                await target_context.send(
                    store["content"],
                    tts=store["tts"],
                    embed=store["embed"],
                    file=store["file"],
                    files=store["files"],
                    delete_after=store["delete_after"],
                    nonce=store["nonce"],
                    allowed_mentions=store["allowed_mentions"]
                )

    # added method
    async def send_store(self, target_context,
                content=None, *, tts=False, embed=None, file=None,
                files=None, delete_after=None, nonce=None,
                allowed_mentions=None):

        if not target_context in self.__store_send_data.keys():
            self.__store_send_data[target_context] = []

        self.__store_send_data[target_context].append({
            "content" : content,
            "tts" : tts,
            "embed" : embed,
            "file" : file,
            "files" : files,
            "delete_after" : delete_after,
            "nonce" : nonce,
            "allowed_mentions" : allowed_mentions
        })
