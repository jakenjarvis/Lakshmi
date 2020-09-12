#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import asyncio
from decimal import Decimal, ROUND_HALF_UP

import LakshmiErrors
from ChoiceReactionFlow import ChoiceReactionFlow
from contents.character.InvestigatorEmbedCreator import InvestigatorEmbedCreator
from contents.character.CharacterManager import CharacterManager
from contents.character.Investigator import Investigator
from contents.FuzzySearchInvestigatorSkills import FuzzySearchInvestigatorSkills

# ;coc character add <URL> サイトのURL指定でキャラ登録
# ;coc character delete <キャラID> キャラIDを指定してキャラ登録情報削除
# ;coc character list 登録済みキャラの一覧表示
# ;coc character urls 登録済みキャラの一覧表示（リンク付き）
# ;coc character choice リストから選択して使用中設定
# ;coc character set image <キャラID> <画像URL> キャラIDを指定して画像URL登録
# ;coc character set change <キャラID> キャラIDを指定して使用中設定
# ;coc character set lost <キャラID> キャラIDを指定してロスト設定
# ;coc character info full <キャラID|active> 指定キャラのステータス表示（フル）
# ;coc character info short <キャラID|active> 指定キャラのステータス表示（簡素）
# ;coc character info backstory <キャラID|active> 指定キャラのステータス表示（キャラ紹介）
# ;coc character info omitted <キャラID|active> 指定キャラのステータス表示（省略）

# TODO:
# :coc skill list スキル名で指定できるスキルリストの表示
# :coc skill find スキル名を探す。
# :coc character get skill <検索文字> 使用中キャラのスキルリスト表示

# :coc character find <検索文字> キャラの検索
# :coc character query skill <query> 条件付き情報表示

# 技能名ダイス、技能検索、技能選択ダイス
# 〇;sp にするとか（pと区別するため)
# spではSANC + アイデア + 知識 + 幸運 + ポイントを振っている技能 を一覧表示させて、リアクションでダイスを降らせる
# pではそれ以外の技能ダイスを振っていただく...とか?
# 〇ｐで数値と文字列両方受け付けて、数値だったらパーセント、文字列だったら技能名から検索して該当するやつでダイス・・・みたいな？

# TODO: embed.set_footerを試す。
# TODO: discord-ext-menusを試す。


class CallOfCthulhuCog(commands.Cog, name='CoC-TRPG系'):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage
        self.manager = CharacterManager(self.bot)

    @commands.group(aliases=['c'])
    async def coc(self, context: commands.Context):
        """詳細は ;help coc で確認してください。"""
        if context.invoked_subcommand is None:
            raise LakshmiErrors.SubcommandNotFoundException()

    @coc.group(aliases=['char','c'])
    async def character(self, context: commands.Context):
        """詳細は ;help coc character で確認してください。"""
        if context.invoked_subcommand is None:
            raise LakshmiErrors.SubcommandNotFoundException()

    @coc.group(aliases=['s'])
    async def skill(self, context: commands.Context):
        """詳細は ;help coc skill で確認してください。"""
        if context.invoked_subcommand is None:
            raise LakshmiErrors.SubcommandNotFoundException()

    @character.command(name='add', aliases=['a'])
    async def character_add(self, context: commands.Context, url: str):
        """ キャラクターシートのURLを指定してLakshmiに登録します。 """
        try:
            result = f""
            await context.trigger_typing()

            character = await self.manager.add_character(context, url)

            result += f"…ふぅ。無事……{character.character_name}さんを登録したわ……。\n"
            result += f"Idは `{character.unique_id}` よ…。"
            await context.send(result)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @character.command(name='delete') # aliases=['del', 'd'] 危険なので省略させない。
    async def character_delete(self, context: commands.Context, unique_id: str):
        """ Lakshmiの登録から指定したキャラクターを削除します。 """
        try:
            result = f""
            await context.trigger_typing()

            character = await self.manager.delete_character(context, unique_id)

            result += f"……ん。無事……{character.character_name}さんを削除……寂しいけど……さようなら……。"
            await context.send(result)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @character.command(name='list', aliases=['l'])
    async def character_list(self, context: commands.Context):
        """ Lakshmiに登録済みのキャラクターシートの一覧を表示します。 """
        try:
            result = f""
            await context.trigger_typing()

            author_name = str(context.author.name)
            display_name = str(context.author.display_name)

            records = await self.manager.get_character_list(context)
            if len(records) >= 1:
                result += f"…ん。あなたの登録キャラクターは次の `{len(records)}人` よ……。"
                result += f"\n"
                result += f"```"
                for record in records:
                    result += f"{record.to_display_string()}\n"
                result += f"```"
            else:
                result += f"あ……。あなたの登録キャラクターが見つからないわ………。"

            await context.send(result)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @character.command(name='urls', aliases=['u'])
    async def character_urls(self, context: commands.Context):
        """ Lakshmiに登録済みのキャラクターシートの一覧（リンク付き）を表示します。 """
        try:
            result = f""
            await context.trigger_typing()

            author_name = str(context.author.name)
            display_name = str(context.author.display_name)

            records = await self.manager.get_character_list(context)
            if len(records) >= 1:
                result += f"…ん。あなたの登録キャラクターは次の `{len(records)}人` よ……。"
                result += f"\n"
                for record in records:
                    result += f"```"
                    result += f"{record.to_display_string()}\n"
                    result += f"```"
                    result += f"　 {record.site_url}\n"
            else:
                result += f"あ……。あなたの登録キャラクターが見つからないわ………。"

            await context.send(result)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @character.command(name='choice', aliases=['c'])
    async def character_choice(self, context: commands.Context):
        """ アクティブなキャラクターを選択したキャラクターに切り替えます。 """
        try:
            # max 30
            master_emojis = [
                "0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣",
                "☮️", "✝️", "☪️", "🕉", "☸️", "✡️", "☯️", "☦️", "♈️", "♉️",
                "♊️", "♋️", "♌️", "♍️", "♎️", "♏️", "♐️", "♑️", "♒️", "♓️"
                ]
            used_emojis = []

            author_name = str(context.author.name)
            display_name = str(context.author.display_name)

            records = await self.manager.get_character_list(context)
            if len(records) >= 1:
                index = 0

                first_send = f""
                first_send += f"…ん。あなたの登録キャラクターは次の `{len(records)}人` よ……。"
                first_send += f"\n"
                first_send += f"```"
                for record in records:
                    first_send += f" {master_emojis[index]} {record.to_display_string()}\n"
                    used_emojis.append(master_emojis[index])
                    index += 1
                first_send += f"```"
                first_send += f"どの子にするの？……切り替えるキャラクターを `30秒以内` に選んで頂戴……。"

                bot_message = await context.send(first_send)

                flow = ChoiceReactionFlow(self.bot, context)
                flow.set_target_message(bot_message, used_emojis)

                emoji = await flow.wait_for_choice_reaction(timeout=30)
                if emoji:
                    chosed_index = used_emojis.index(emoji)
                    chosed_character = records[chosed_index]

                    unique_id = chosed_character.unique_id
                    records = await self.manager.set_character_active(context, unique_id)

                    result = f"…ふぅ。{records.character_name}さんをアクティブに設定したわ……。"
                    await context.send(result)
                else:
                    result = f'時間切れよ………{context.author.display_name}さんは優柔不断ね……。'
                    await context.send(result)
            else:
                result = f"あ……。あなたの登録キャラクターが見つからないわ………。"
                await context.send(result)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @character.group(aliases=['s'])
    async def set(self, context: commands.Context):
        """詳細は ;help coc character set で確認してください。"""
        if context.invoked_subcommand is None:
            raise LakshmiErrors.SubcommandNotFoundException()

    @set.command(name='image', aliases=['img', 'i'])
    async def set_image(self, context: commands.Context, unique_id: str, image_url: str):
        """ キャラクターと画像URLを指定して、指定したキャラクターのイメージ画像を登録します。 """
        try:
            result = f""
            await context.trigger_typing()

            records = await self.manager.set_character_image(context, unique_id, image_url)

            result += f"…ん。{records.character_name}さんの画像を登録したわ……。"
            await context.send(result)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @set.command(name='change', aliases=['c'])
    async def set_change(self, context: commands.Context, unique_id: str):
        """ アクティブなキャラクターを指定したキャラクターに切り替えます。 """
        try:
            result = f""
            await context.trigger_typing()

            records = await self.manager.set_character_active(context, unique_id)

            result += f"…ふぅ。{records.character_name}さんをアクティブに設定したわ……。"
            await context.send(result)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @set.command(name='lost', aliases=['l'])
    async def set_lost(self, context: commands.Context, unique_id: str):
        """ 指定したキャラクターをロスト状態に設定します（戻せません）。 """
        try:
            result = f""
            await context.trigger_typing()

            records = await self.manager.set_character_lost(context, unique_id)

            result += f"…あぅ。ロスト設定したわ……。{records.character_name}さんのご冥福をお祈りいたします……。"
            await context.send(result)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @character.group(aliases=['i'])
    async def info(self, context: commands.Context):
        """詳細は ;help coc character info で確認してください。"""
        if context.invoked_subcommand is None:
            raise LakshmiErrors.SubcommandNotFoundException()

    @info.command(name='full', aliases=['f'])
    async def info_full(self, context: commands.Context, unique_id: str = ""):
        """ キャラクターシートのIDを指定して情報（Full）を表示します。 """
        try:
            await context.trigger_typing()

            character = await self.manager.get_character_information(context, unique_id)

            embed = InvestigatorEmbedCreator.create_full_status(character)

            # 画像リンクの有効性をチェックして警告表示を入れる。
            if len(character.image_url) >= 1:
                if not await self.manager.is_image_url(character.image_url):
                    out_value = f"…むぅ。画像URLのリンク先……見つからないわ……。もう一度登録しなおしてみて……。\n"
                    out_value += f"{character.image_url}"
                    embed.add_field(name="警告", value=out_value, inline=False)

            await context.send(embed=embed)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @info.command(name='short', aliases=['s'])
    async def info_short(self, context: commands.Context, unique_id: str = ""):
        """ キャラクターシートのIDを指定して情報（short）を表示します。 """
        try:
            await context.trigger_typing()

            character = await self.manager.get_character_information(context, unique_id)

            embed = InvestigatorEmbedCreator.create_short_status(character)

            # 画像リンクの有効性をチェックして警告表示を入れる。
            if len(character.image_url) >= 1:
                if not await self.manager.is_image_url(character.image_url):
                    out_value = f"…むぅ。画像URLのリンク先……見つからないわ……。もう一度登録しなおしてみて……。\n"
                    out_value += f"{character.image_url}"
                    embed.add_field(name="警告", value=out_value, inline=False)

            await context.send(embed=embed)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @info.command(name='backstory', aliases=['back', 'story', 'bs', 'b'])
    async def info_backstory(self, context: commands.Context, unique_id: str = ""):
        """ キャラクターシートのIDを指定して情報（backstory）を表示します。 """
        try:
            await context.trigger_typing()

            character = await self.manager.get_character_information(context, unique_id)

            embed = InvestigatorEmbedCreator.create_backstory_status(character)

            # 画像リンクの有効性をチェックして警告表示を入れる。
            if len(character.image_url) >= 1:
                if not await self.manager.is_image_url(character.image_url):
                    out_value = f"…むぅ。画像URLのリンク先……見つからないわ……。もう一度登録しなおしてみて……。\n"
                    out_value += f"{character.image_url}"
                    embed.add_field(name="警告", value=out_value, inline=False)

            await context.send(embed=embed)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @info.command(name='omitted', aliases=['o'])
    async def info_omitted(self, context: commands.Context, unique_id: str = ""):
        """ キャラクターシートのIDを指定して情報（omitted）を表示します。 """
        try:
            await context.trigger_typing()

            character = await self.manager.get_character_information(context, unique_id)

            embed = InvestigatorEmbedCreator.create_omitted_status(character)

            # 画像リンクの有効性をチェックして警告表示を入れる。
            if len(character.image_url) >= 1:
                if not await self.manager.is_image_url(character.image_url):
                    out_value = f"…むぅ。画像URLのリンク先……見つからないわ……。もう一度登録しなおしてみて……。\n"
                    out_value += f"{character.image_url}"
                    embed.add_field(name="警告", value=out_value, inline=False)

            await context.send(embed=embed)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

    @skill.command(name='find', aliases=['f'])
    async def skill_find(self, context: commands.Context, *, keyword: str):
        """ アクティブキャラのスキルから、該当するスキルをあいまい検索します。 """
        try:
            result = f""
            await context.trigger_typing()

            author_name = str(context.author.name)
            display_name = str(context.author.display_name)

            character = await self.manager.get_character_information(context, "")

            search_skills = FuzzySearchInvestigatorSkills(character)

            items = search_skills.search(keyword)
            if len(items) >= 1:
                result += f"…ん。{character.character_name}さんのスキルから `{keyword}` をあいまい検索した結果は、次の `{len(items)}件` よ……。"
                result += f"\n"
                result += f"```"
                for item in items:
                    max_main_distance = item.max_main_distance.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
                    max_sub_distance = item.max_sub_distance.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
                    sum_distance = item.sum_distance.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
                    result += f"{sum_distance}: {item.link_name} = [{item.main_name}({max_main_distance})], [{item.sub_name}({max_sub_distance})]\n"
                result += f"```"

                if len(items[0].sub_name) >= 1:
                    pickskillname = f"{items[0].main_name}({items[0].sub_name})"
                else:
                    pickskillname = f"{items[0].main_name}"
                result += f"あえて選ぶなら・・・ `{pickskillname}` かしら……。"
            else:
                result += f"あ……。該当するスキルを見つけられなかったわ………。"

            await context.send(result)

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

def setup(bot):
    bot.add_cog(CallOfCthulhuCog(bot))
