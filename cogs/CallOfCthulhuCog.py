#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

from LakshmiErrors import CharacterNotFoundException

from contents.CharacterVampireBloodNetGetter import CharacterVampireBloodNetGetter

class CallOfCthulhuCog(commands.Cog, name='CoC-TRPG系'):
    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

    @commands.command()
    async def request(self, context: commands.Context, url: str):
        """テスト"""
        try:
            result = ""
            await context.trigger_typing()

            getter = CharacterVampireBloodNetGetter()
            character = getter.request(url)
            if character:
                print(character.name)
                #result = f'{context.author.mention} {character.name} {character.age} {character.sex} {character.occupation}\n{character.memo}'
                #await context.send(result)

                onelinebackstory = character.backstory.splitlines()[0]

                embed = discord.Embed(
                    title=f"{character.name} - `{character.occupation}` {character.sex}({character.age}歳)",
                    description=f"{onelinebackstory}"
                    )
                embed.set_author(name=f"{character.name}",url=f"{character.site_url}",icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
                embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")

                # 情報
                out_value = f""
                out_value += f"`身長: {character.personal_data.height}`　`体重: {character.personal_data.weight}`　`髪: {character.personal_data.hair_color}`　`瞳: {character.personal_data.eye_color}`　`肌: {character.personal_data.skin_color}`\n"
                if len(character.tag) >= 1:
                    out_value += f"**TAG:** `{character.tag.replace(' ','`　`')}`"
                embed.add_field(name="その他情報", value=out_value, inline=False)

                # 基礎能力、特性等
                embed.add_field(name="能力値",value=f"STR: {character.STR}　CON: {character.CON}　POW: {character.POW}　DEX: {character.DEX}　APP: {character.APP}　SIZ: {character.SIZ}　INT: {character.INT}　EDU: {character.EDU}",inline=False)
                embed.add_field(name="特性",value=f"HP: {character.HP}　MP: {character.MP}　SAN値: {character.SAN}　アイデア: {character.IDEA}　幸運: {character.LUCK}　知識: {character.KNOWLEDGE}",inline=False)

                # 戦闘技能
                out_value = f""
                for key in character.combat_skills.keys():
                    if len(character.combat_skills[key].skill_subname) >= 1:
                        out_value += f"{character.combat_skills[key].skill_name}({character.combat_skills[key].skill_subname}): {character.combat_skills[key].current}　"
                    else:
                        out_value += f"{character.combat_skills[key].skill_name}: {character.combat_skills[key].current}　"
                embed.add_field(name="戦闘技能", value=out_value, inline=False)

                # 探索技能
                out_value = f""
                for key in character.search_skills.keys():
                    if len(character.search_skills[key].skill_subname) >= 1:
                        out_value += f"{character.search_skills[key].skill_name}({character.search_skills[key].skill_subname}): {character.search_skills[key].current}　"
                    else:
                        out_value += f"{character.search_skills[key].skill_name}: {character.search_skills[key].current}　"
                embed.add_field(name="探索技能", value=out_value, inline=False)

                # 行動技能
                out_value = f""
                for key in character.behavioral_skills.keys():
                    if len(character.behavioral_skills[key].skill_subname) >= 1:
                        out_value += f"{character.behavioral_skills[key].skill_name}({character.behavioral_skills[key].skill_subname}): {character.behavioral_skills[key].current}　"
                    else:
                        out_value += f"{character.behavioral_skills[key].skill_name}: {character.behavioral_skills[key].current}　"
                embed.add_field(name="行動技能", value=out_value, inline=False)

                # 交渉技能
                out_value = f""
                for key in character.negotiation_skills.keys():
                    if len(character.negotiation_skills[key].skill_subname) >= 1:
                        out_value += f"{character.negotiation_skills[key].skill_name}({character.negotiation_skills[key].skill_subname}): {character.negotiation_skills[key].current}　"
                    else:
                        out_value += f"{character.negotiation_skills[key].skill_name}: {character.negotiation_skills[key].current}　"
                embed.add_field(name="交渉技能", value=out_value, inline=False)

                # 知識技能
                out_value = f""
                for key in character.knowledge_skills.keys():
                    if len(character.knowledge_skills[key].skill_subname) >= 1:
                        out_value += f"{character.knowledge_skills[key].skill_name}({character.knowledge_skills[key].skill_subname}): {character.knowledge_skills[key].current}　"
                    else:
                        out_value += f"{character.knowledge_skills[key].skill_name}: {character.knowledge_skills[key].current}　"
                embed.add_field(name="知識技能", value=out_value, inline=False)

                await context.send(embed=embed)
            else:
                raise CharacterNotFoundException()

        except Exception as e:
            # エラー検知時通知
            await self.bot.on_command_error(context, e)

def setup(bot):
    bot.add_cog(CallOfCthulhuCog(bot))
