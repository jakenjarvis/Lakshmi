#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import random
import math
import datetime
import pytz

import discord

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
class LakshmiLexicon():
    MATCH_OHAYO = re.compile(r"(おはよう|おっはよ(ー|～)?|おっは(ー|～)?|おはよ(ー|～)?|^おは(ー|～)?$)", re.IGNORECASE)
    MATCH_OYASUMI = re.compile(r"(おやすみなさい|おやすみ(ー|～)?)", re.IGNORECASE)
    MATCH_KONCHIWA = re.compile(r"(こんにち(わ|は)(ー|～)?|こんち(わ|は|ゃ)(ー|～)?)", re.IGNORECASE)
    MATCH_KONBANWA = re.compile(r"(こんばん(わ|は|にゃ|にゃ(ぁ|あ))(ー|～)?|ばん(わ|は|にゃ|にゃ(ぁ|あ))(ー|～)?|^こん(ー|～)?$)", re.IGNORECASE)

    def __init__(self, bot):
        self.bot = bot
        #self.bot.storage

        # 最終挨拶発言者別日時記録
        self.last_say_hello = {}

        self.character_command_not_found_dialogue = [
            "…ん。入力ミスを感知。私、アップルパイを焼いてるところだから、あなたが直しておいてね。",
            "…むぅ。入力ミスを感知。でも…私、もう限界…。あとはあなたに任せた…。( ˘ω˘)ｽﾔｧ……あっ、いけない…寝てた…。",
            "…あ。入力ミスを感知。…あれ、目を離した隙に私の林檎が（ｷｮﾛｷｮﾛ)。私が林檎を探している間に直しておいて。…さて、林檎林檎（ｷｮﾛｷｮﾛ）",
            "…お。入力ミスを感知。そんなことより、きょ…今日から深夜アニメに挑戦よ…。あなたが入力ミスを直している間に、全話見てあげるからね。",
            "…あ。入力ミスを感知。それよりもこのクマのぬいぐるみ…これは買いね……。私がこれを買う間に入力ミスを直しておいてね。あぁ…、このクマ最高……( ˘ω˘)♡",
            "あなたの文字が何かわからなかったせいで、今、私はヨガみたいなポーズをとらされているわ……ダイスなんて振れない！",
            "…ひっ…入力ミスがあるわ…。私は『くとぅるふ』の 『るーるぶっく』を読んでるから…あなたは入力ミスを直しておいて。…私も探索してみたいな…。",
            "…ん。入力ミスを感知。(ﾓｸﾞﾓｸﾞ)焼きリンゴも案外悪くないわね……あつ…。あなたも入力ミスを直し終わったら食べさせてあげるからね。",
            #"…今のは何だろう…？　私がファンブル連発したら『おはシュミ』と、いわれるのかしら…。私がファンブルの具現化なんて…やだ…。",
            "…ん。入力ミスがあったみたい。私が読める字で書き直してね？",
            "…むぅ。あなたの入力ミスのせいで、処理ができなかった。…どう責任取ってくれるの？",
            "(ﾓｸﾞﾓｸﾞ)…林檎に夢中で、処理工程を見ていなかったけど…。入力ミスをしているわね。ちゃんと確認してみて。",
        ]

    # --------------------------------------------------------------------------------
    # Common
    # --------------------------------------------------------------------------------
    def get_jst_datetime_now(self):
        return datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

    # --------------------------------------------------------------------------------
    # Greeting Messages
    # --------------------------------------------------------------------------------
    def get_character_message_for_command_nagisa(self):
        return "…ん。お望みの **形態素解析結果** よ……。"

    def get_character_message_for_command_hello(self):
        return "はぁい…………。ちゃんといるわよ……。"

    def is_say_hello(self, message):
        result = False
        if LakshmiLexicon.MATCH_KONCHIWA.search(message.content):
            # こんにちは
            result = True
        elif LakshmiLexicon.MATCH_KONBANWA.search(message.content):
            # こんばんは
            result = True
        elif LakshmiLexicon.MATCH_OHAYO.search(message.content):
            # おはよう
            result = True
        elif LakshmiLexicon.MATCH_OYASUMI.search(message.content):
            # おやすみ
            result = True

        # 最近発言したばかりの場合は、発言を控える。
        if message.author.id in self.last_say_hello.keys():
            yuuyo = self.last_say_hello[message.author.id] + datetime.timedelta(minutes=30)
            if self.get_jst_datetime_now() <= yuuyo:
                result = False
        return result

    def get_character_message_for_greeting_text(self, message: discord.Message):
        result = ""

        # チャンネルに参加しているオンラインメンバーも扱う
        target_members = [
            member for member in message.channel.members
            if (member != message.author)
                and (member != self.bot.user)
                and (member.status == discord.Status.online)
                and (
                    (not member.id in self.last_say_hello)
                    or (self.get_jst_datetime_now() > self.last_say_hello[member.id] + datetime.timedelta(minutes=30)
                    )
                )
            ]

        # 記録
        self.last_say_hello[message.author.id] = self.get_jst_datetime_now()
        for member in target_members:
            self.last_say_hello[member.id] = self.get_jst_datetime_now()

        # now.hour   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
        timetable = [3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2]
        #            0:お昼時 1:朝方 2:夜間 3:真夜中
        target = timetable[self.last_say_hello[message.author.id].hour]
        message_table = []
        if LakshmiLexicon.MATCH_KONCHIWA.search(message.content):
            # こんにちは
            message_table.append(f'{message.author.display_name}さん。……こんにちは。') # 0:お昼時
            message_table.append(f'おはよう……。{message.author.display_name}さん、おはやいのね。') # 1:朝方
            message_table.append(f'こんばんは。{message.author.display_name}さん…………もう夜の時間よ？') # 2:夜間
            message_table.append(f'…むぅ。{message.author.display_name}さん、疲れているようね……。林檎を抱いて寝なさい……。') # 3:真夜中
        elif LakshmiLexicon.MATCH_KONBANWA.search(message.content):
            # こんばんは
            message_table.append(f'こんにちは。{message.author.display_name}さん、もうお昼よ？昼夜が逆転してるじゃない……。') # 0:お昼時
            message_table.append(f'…むぅ。{message.author.display_name}さん、疲れているようね……。林檎を食べて元気だして……。') # 1:朝方
            message_table.append(f'{message.author.display_name}さん。……こんばんは。') # 2:夜間
            message_table.append(f'{message.author.display_name}さん。こんばんは……もう寝ないと朝が大変よ……。') # 3:真夜中
        elif LakshmiLexicon.MATCH_OHAYO.search(message.content):
            # おはよう
            message_table.append(f'こんにちは、{message.author.display_name}さん。お寝坊さんね。') # 0:お昼時
            message_table.append(f'{message.author.display_name}さん。……おはよう。朝は辛いの……。') # 1:朝方
            message_table.append(f'こんばんは。…ねぇ。{message.author.display_name}さん、時間感覚が狂ってるわよ？心配になるわ……。') # 2:夜間
            message_table.append(f'…もぅ。{message.author.display_name}さん、昼夜が逆転してるわ……。体に気を付けて……。') # 3:真夜中
        elif LakshmiLexicon.MATCH_OYASUMI.search(message.content):
            # おやすみ
            message_table.append(f'こんにちは。{message.author.display_name}さん。お昼寝するの？') # 0:お昼時
            message_table.append(f'…もぅ。{message.author.display_name}さん、昼夜が逆転してるわ……。ゆっくり休んでね……。') # 1:朝方
            message_table.append(f'{message.author.display_name}さん、おやすみなさい。甘い林檎の良い夢を……。') # 2:夜間
            message_table.append(f'{message.author.display_name}さん、おやすみなさい。私ももう寝るわ……。') # 3:真夜中

        result += message_table[target]

        additional_members_message = f""
        if len(target_members) == 0:
            additional_members_message = f""
        elif len(target_members) == 1:
            additional_members_message = f"{target_members[0].display_name}さんも、"
        elif len(target_members) == 2:
            additional_members_message = f"{target_members[0].display_name}さんと{target_members[1].display_name}さんも、"
        else:
            additional_members_message = f"みんなも"

        message_table2 = []
        message_table2.append(f'{additional_members_message}こんにちは……。') # 0:お昼時
        message_table2.append(f'{additional_members_message}おはよう……。') # 1:朝方
        message_table2.append(f'{additional_members_message}こんばんは……。') # 2:夜間
        message_table2.append(f'{additional_members_message}こんばんは……みんな、もう寝ましょう……？') # 3:真夜中

        if len(target_members) >= 1:
            result += message_table2[target]

        return result

    def get_character_message_when_talked_to_by_mention(self):
        # 話しかけられた時のメッセージ
        return "……ん？私を………呼んだ？"

    # --------------------------------------------------------------------------------
    # Exception Messages
    # --------------------------------------------------------------------------------

    def get_character_message_for_command_not_found(self):
        # 存在しないコマンドが指定されたときのエラーメッセージ
        return random.choice(self.character_command_not_found_dialogue)

    def get_character_message_for_argument_out_of_range_exception(self):
        # パラメータの範囲が指定範囲を超えたときのエラーメッセージ
        return "ごめんなさい……おっきくて、計算できないの……"

    def get_character_message_for_permission_not_found_exception(self):
        # 指定したコマンドの実行権限がない場合のエラーメッセージ
        return "あなた……権限が無いみたいよ………。"

    def get_character_message_for_missing_required_argument(self):
        # パラメータが足りなくて処理できないときのエラーメッセージ
        return "ちょっと……これで………どうしろというの？"

    def get_character_message_to_ask_the_developer_for_help(self):
        # 原因不明のエラーで開発者に助けを求めるときのエラーメッセージ
        return "私の中で……何かが起こったようなの………。これを……開発者さんに知らせてあげて！"

    def get_character_message_for_unsupported_sites(self):
        # 対応していないサイトのURLが指定されたときのエラーメッセージ
        return "…むぅ。私はそのサイト………知らないわ……。ごめんなさい………。"

    def get_character_message_for_not_callofcthulhu_investigator(self):
        # 対応していないサイトのURLが指定されたときのエラーメッセージ
        return "…あ。クトゥルフの探索者じゃないキャラは扱えないわ……。ごめんなさい………。"

    def get_character_message_for_character_not_found(self):
        # 存在しないキャラクターが指定されたときのエラーメッセージ
        return "ねぇ……。そのキャラクター……見つからないわ………何か間違ってない？"

    def get_character_message_for_image_not_found(self):
        # 存在しない画像が指定されたときのエラーメッセージ
        return "…むぅ。その画像……見つからないわ………もう一度ちゃんと確認してみて……。"
