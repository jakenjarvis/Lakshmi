#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict
import math
import random
import aiohttp
import asyncio

import discord
from discord.ext import commands, tasks

from contents.character.Investigator import Investigator

class CharacterOccupation():
    def __init__(self, occupation: str):
        # 職業
        self.occupation = occupation

        # 職業別データ
        self.occupations = {
            "doctor_of_medicine" : {
                "basename" : "医師",
                "confirmed_list" : ["medicine", "first_aid", "credit_rating", "psychology", "psychoanalysis", "biology", "other_language(ラテン語)", "pharmacy"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "selfish",           # 自己利益優先的な性格
                    "responsible",       # 責任感のある性格
                    "serious",           # 真面目で少々固い性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "nervous",           # 神経質で臆病な性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "jealous",           # 嫉妬しやすい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "gentle",            # 穏やかで優しい性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "engineer" : {
                "basename" : "エンジニア",
                "confirmed_list" : ["chemistry", "mech_repair", "opr_hvy_machine", "electr_repair", "geology", "library_use", "physics"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "serious",           # 真面目で少々固い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "nervous",           # 神経質で臆病な性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "jealous",           # 嫉妬しやすい性格
                    "responsible",       # 責任感のある性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "gentle",            # 穏やかで優しい性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "selfish",           # 自己利益優先的な性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "entertainer" : {
                "basename" : "エンターテイナー",
                "confirmed_list" : ["fast_talk", "dodge", "listen", "art(*)", "credit_rating", "psychology", "disguise"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "jealous",           # 嫉妬しやすい性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "selfish",           # 自己利益優先的な性格
                    "gentle",            # 穏やかで優しい性格
                    "responsible",       # 責任感のある性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "nervous",           # 神経質で臆病な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "serious",           # 真面目で少々固い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "professor" : {
                "basename" : "教授",
                "confirmed_list" : ["credit_rating", "psychology", "persuade", "library_use", "bargain", "other_language(*)"],
                "2_choice_skills" : ["medicine", "chemistry", "archeology", "anthropology", "biology", "geology", "electronics", "astronomy", "natural_history", "physics", "law", "history"],
                "undetermined_skills": 0,
                "personalitys": [
                    "selfish",           # 自己利益優先的な性格
                    "jealous",           # 嫉妬しやすい性格
                    "serious",           # 真面目で少々固い性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "gentle",            # 穏やかで優しい性格
                    "nervous",           # 神経質で臆病な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "responsible",       # 責任感のある性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "zealot" : {
                "basename" : "狂信者",
                "confirmed_list" : ["conceal", "hide", "psychology", "persuade", "library_use"],
                "2_choice_skills" : ["chemistry", "electr_repair", "law", "pharmacy", "rifle"],
                "undetermined_skills": 1,
                "personalitys": [
                    "responsible",       # 責任感のある性格
                    "serious",           # 真面目で少々固い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "nervous",           # 神経質で臆病な性格
                    "jealous",           # 嫉妬しやすい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "gentle",            # 穏やかで優しい性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "selfish",           # 自己利益優先的な性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "military_officer" : {
                "basename" : "軍仕官",
                "confirmed_list" : ["accounting", "credit_rating", "psychology", "persuade", "navigate", "bargain", "law"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "responsible",       # 責任感のある性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "serious",           # 真面目で少々固い性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "gentle",            # 穏やかで優しい性格
                    "nervous",           # 神経質で臆病な性格
                    "jealous",           # 嫉妬しやすい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "selfish",           # 自己利益優先的な性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "policeman" : {
                "basename" : "警官",
                "confirmed_list" : ["fast_talk", "first_aid", "dodge", "grapple", "psychology", "law"],
                "2_choice_skills" : ["drive(自動車)", "ride", "bargain", "martial_arts", "spot_hidden"],
                "undetermined_skills": 0,
                "personalitys": [
                    "bravepatient",      # 勇敢で我慢強い性格
                    "responsible",       # 責任感のある性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "serious",           # 真面目で少々固い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "gentle",            # 穏やかで優しい性格
                    "nervous",           # 神経質で臆病な性格
                    "jealous",           # 嫉妬しやすい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "selfish",           # 自己利益優先的な性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "police_detective" : {
                "basename" : "刑事",
                "confirmed_list" : ["fast_talk", "listen", "psychology", "persuade", "bargain", "law", "spot_hidden"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "responsible",       # 責任感のある性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "serious",           # 真面目で少々固い性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "gentle",            # 穏やかで優しい性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "nervous",           # 神経質で臆病な性格
                    "jealous",           # 嫉妬しやすい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "selfish",           # 自己利益優先的な性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "artist" : {
                "basename" : "芸術家",
                "confirmed_list" : ["fast_talk", "art(*)", "photography", "psychology", "craft(*)", "spot_hidden", "history"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "nervous",           # 神経質で臆病な性格
                    "jealous",           # 嫉妬しやすい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "gentle",            # 穏やかで優しい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "selfish",           # 自己利益優先的な性格
                    "serious",           # 真面目で少々固い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "responsible",       # 責任感のある性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "antiquarian" : {
                "basename" : "古物研究家",
                "confirmed_list" : ["art(*)", "craft(*)", "library_use", "bargain", "other_language(*)", "spot_hidden", "history"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "jealous",           # 嫉妬しやすい性格
                    "selfish",           # 自己利益優先的な性格
                    "nervous",           # 神経質で臆病な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "serious",           # 真面目で少々固い性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "gentle",            # 穏やかで優しい性格
                    "responsible",       # 責任感のある性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "author" : {
                "basename" : "作家",
                "confirmed_list" : ["occult", "psychology", "persuade", "library_use", "other_language(*)", "own_language(*)", "history"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "nervous",           # 神経質で臆病な性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "jealous",           # 嫉妬しやすい性格
                    "gentle",            # 穏やかで優しい性格
                    "responsible",       # 責任感のある性格
                    "selfish",           # 自己利益優先的な性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "serious",           # 真面目で少々固い性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "journalist" : {
                "basename" : "ジャーナリスト",
                "confirmed_list" : ["fast_talk", "photography", "psychology", "persuade", "library_use", "own_language(*)", "history"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "bravepatient",      # 勇敢で我慢強い性格
                    "responsible",       # 責任感のある性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "serious",           # 真面目で少々固い性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "gentle",            # 穏やかで優しい性格
                    "nervous",           # 神経質で臆病な性格
                    "jealous",           # 嫉妬しやすい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "selfish",           # 自己利益優先的な性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "private_investigator" : {
                "basename" : "私立探偵",
                "confirmed_list" : ["fast_talk", "locksmith", "photography", "psychology", "library_use", "bargain", "law"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "selfish",           # 自己利益優先的な性格
                    "responsible",       # 責任感のある性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "serious",           # 真面目で少々固い性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "gentle",            # 穏やかで優しい性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "nervous",           # 神経質で臆病な性格
                    "jealous",           # 嫉妬しやすい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "spokesperson" : {
                "basename" : "スポークスマン",
                "confirmed_list" : ["fast_talk", "dodge", "credit_rating", "psychology", "persuade", "disguise"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "talkative",         # おしゃべりで口数が多い性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "gentle",            # 穏やかで優しい性格
                    "responsible",       # 責任感のある性格
                    "serious",           # 真面目で少々固い性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "nervous",           # 神経質で臆病な性格
                    "jealous",           # 嫉妬しやすい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "selfish",           # 自己利益優先的な性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "athlete" : {
                "basename" : "スポーツ選手",
                "confirmed_list" : ["dodge", "ride", "swim", "jump", "throw", "climb", "martial_arts"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "bravepatient",      # 勇敢で我慢強い性格
                    "selfish",           # 自己利益優先的な性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "gentle",            # 穏やかで優しい性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "responsible",       # 責任感のある性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "nervous",           # 神経質で臆病な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "serious",           # 真面目で少々固い性格
                    "jealous",           # 嫉妬しやすい性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "clergyman" : {
                "basename" : "聖職者",
                "confirmed_list" : ["listen", "accounting", "psychology", "persuade", "library_use", "other_language(*)", "history"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "responsible",       # 責任感のある性格
                    "serious",           # 真面目で少々固い性格
                    "gentle",            # 穏やかで優しい性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "nervous",           # 神経質で臆病な性格
                    "jealous",           # 嫉妬しやすい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "selfish",           # 自己利益優先的な性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "parapsychologist" : {
                "basename" : "超心理学者",
                "confirmed_list" : ["occult", "anthropology", "photography", "psychology", "library_use", "history", "other_language(*)"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "serious",           # 真面目で少々固い性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "gentle",            # 穏やかで優しい性格
                    "nervous",           # 神経質で臆病な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "selfish",           # 自己利益優先的な性格
                    "jealous",           # 嫉妬しやすい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "responsible",       # 責任感のある性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "dilettante" : {
                "basename" : "ディレッタント",
                "confirmed_list" : ["art(*)", "ride", "shotgun", "credit_rating", "craft(*)", "other_language(*)"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "nervous",           # 神経質で臆病な性格
                    "selfish",           # 自己利益優先的な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "jealous",           # 嫉妬しやすい性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "gentle",            # 穏やかで優しい性格
                    "responsible",       # 責任感のある性格
                    "serious",           # 真面目で少々固い性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "missionary" : {
                "basename" : "伝道者",
                "confirmed_list" : ["medicine", "first_aid", "mech_repair", "art(*)", "persuade", "natural_history"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "talkative",         # おしゃべりで口数が多い性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "gentle",            # 穏やかで優しい性格
                    "responsible",       # 責任感のある性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "nervous",           # 神経質で臆病な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "serious",           # 真面目で少々固い性格
                    "jealous",           # 嫉妬しやすい性格
                    "selfish",           # 自己利益優先的な性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "tribal_member" : {
                "basename" : "トライブ・メンバー",
                "confirmed_list" : ["occult", "listen", "swim", "throw", "bargain", "natural_history", "spot_hidden"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "selfish",           # 自己利益優先的な性格
                    "responsible",       # 責任感のある性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "gentle",            # 穏やかで優しい性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "serious",           # 真面目で少々固い性格
                    "nervous",           # 神経質で臆病な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "jealous",           # 嫉妬しやすい性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "farmer_forester" : {
                "basename" : "農林業作業者",
                "confirmed_list" : ["first_aid", "mech_repair", "opr_hvy_machine", "craft(*)", "track", "electr_repair", "natural_history"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "responsible",       # 責任感のある性格
                    "serious",           # 真面目で少々固い性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "selfish",           # 自己利益優先的な性格
                    "jealous",           # 嫉妬しやすい性格
                    "nervous",           # 神経質で臆病な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "gentle",            # 穏やかで優しい性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "pilot" : {
                "basename" : "パイロット",
                "confirmed_list" : ["mech_repair", "opr_hvy_machine", "electr_repair", "pilot(*)", "astronomy", "navigate", "physics"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "responsible",       # 責任感のある性格
                    "serious",           # 真面目で少々固い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "nervous",           # 神経質で臆病な性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "gentle",            # 穏やかで優しい性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "selfish",           # 自己利益優先的な性格
                    "jealous",           # 嫉妬しやすい性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "hacker_consultant" : {
                "basename" : "ハッカー/コンサルタント",
                "confirmed_list" : ["fast_talk", "computer", "electr_repair", "electronics", "library_use", "psychology", "other_language(*)"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "selfish",           # 自己利益優先的な性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "nervous",           # 神経質で臆病な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "jealous",           # 嫉妬しやすい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "serious",           # 真面目で少々固い性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "responsible",       # 責任感のある性格
                    "gentle",            # 穏やかで優しい性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "criminal" : {
                "basename" : "犯罪者",
                "confirmed_list" : ["fast_talk", "locksmith", "handgun", "sneak", "bargain", "disguise", "spot_hidden"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "lazyloose",         # 怠惰でだらしない性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "selfish",           # 自己利益優先的な性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "jealous",           # 嫉妬しやすい性格
                    "nervous",           # 神経質で臆病な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "gentle",            # 穏やかで優しい性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "serious",           # 真面目で少々固い性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "responsible",       # 責任感のある性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "soldier" : {
                "basename" : "兵士",
                "confirmed_list" : ["first_aid", "dodge", "conceal", "mech_repair", "listen", "sneak", "rifle"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "bravepatient",      # 勇敢で我慢強い性格
                    "responsible",       # 責任感のある性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "nervous",           # 神経質で臆病な性格
                    "serious",           # 真面目で少々固い性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "jealous",           # 嫉妬しやすい性格
                    "gentle",            # 穏やかで優しい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "selfish",           # 自己利益優先的な性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "lawyer" : {
                "basename" : "弁護士",
                "confirmed_list" : ["fast_talk", "credit_rating", "psychology", "persuade", "library_use", "bargain", "law"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "polite",            # 礼儀正しく丁寧な性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "selfish",           # 自己利益優先的な性格
                    "serious",           # 真面目で少々固い性格
                    "responsible",       # 責任感のある性格
                    "nervous",           # 神経質で臆病な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "gentle",            # 穏やかで優しい性格
                    "jealous",           # 嫉妬しやすい性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "drifter" : {
                "basename" : "放浪者",
                "confirmed_list" : ["fast_talk", "hide", "listen", "sneak", "psychology", "bargain", "natural_history"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "lazyloose",         # 怠惰でだらしない性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "nervous",           # 神経質で臆病な性格
                    "selfish",           # 自己利益優先的な性格
                    "jealous",           # 嫉妬しやすい性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "entertaining",      # 人を楽しませるような面白い性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "gentle",            # 穏やかで優しい性格
                    "serious",           # 真面目で少々固い性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "responsible",       # 責任感のある性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
            "musician" : {
                "basename" : "ミュージシャン",
                "confirmed_list" : ["fast_talk", "listen", "art(*)", "craft(*)", "persuade", "psychology", "bargain"],
                "2_choice_skills" : [],
                "undetermined_skills": 1,
                "personalitys": [
                    "entertaining",      # 人を楽しませるような面白い性格
                    "talkative",         # おしゃべりで口数が多い性格
                    "nervous",           # 神経質で臆病な性格
                    "sensitive",         # 繊細で傷つきやすい性格
                    "selfish",           # 自己利益優先的な性格
                    "jealous",           # 嫉妬しやすい性格
                    "evilchildish",      # 意地悪で子供っぽい性格
                    "lazyloose",         # 怠惰でだらしない性格
                    "gentle",            # 穏やかで優しい性格
                    "bravepatient",      # 勇敢で我慢強い性格
                    "polite",            # 礼儀正しく丁寧な性格
                    "responsible",       # 責任感のある性格
                    "honest",            # 正直で嘘をつかない誠実な性格
                    "serious",           # 真面目で少々固い性格
                    "unique",            # とても変わった例えようのない珍しい性格
                ],
            },
        }

    def get_key(self) -> str:
        return self.occupation

    def get_name(self) -> str:
        return self.occupations[self.occupation]["basename"]

    def get_confirmed_list(self) -> List[str]:
        return self.occupations[self.occupation]["confirmed_list"]

    def get_2_choice_skills(self) -> List[str]:
        return self.occupations[self.occupation]["2_choice_skills"]

    def get_undetermined_skills(self) -> int:
        return self.occupations[self.occupation]["undetermined_skills"]


    def choice_personality(self, occupation: str) -> str:
        # 職業別の性格リストから上位の物を優先的に選択する。
        targetlist = self.occupations[occupation]["personalitys"]
        weights = list(reversed([math.ceil(_ / 1) for _ in range(1, len(targetlist)+1)]))
        return random.choices(targetlist, weights=weights, k=1)[0]

