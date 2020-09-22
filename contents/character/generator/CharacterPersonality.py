#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Callable
import math
import random

class CharacterPersonality(): # individuality?
    def __init__(self):
        # 性格
        # https://mysuki.jp/english-personality-5486
        # https://harahara.net/English/resources/personality.htm
        # スキルの「選択の仕方」に影響を与えるものとする。
        self.personalitys = {
            "serious": {
                "description": "真面目で少々固い性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 1.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 1.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 8, "new_count": 1 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(100 / x * 0.8) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(100 / x * 0.8) for x in range(1, n+1)],
            },
            "honest": {
                "description": "正直で嘘をつかない誠実な性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 1.5,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 1.5,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 6, "new_count": 3 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(100 / x * 0.9) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(100 / x * 0.9) for x in range(1, n+1)],
            },
            "bravepatient": {
                "description": "勇敢で我慢強い性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 3.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 1.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 5, "new_count": 3 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
            },
            "responsible": {
                "description": "責任感のある性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 1.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 3.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 8, "new_count": 0 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
            },
            "gentle": {
                "description": "穏やかで優しい性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 1.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 4.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 5, "new_count": 5 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
            },
            "polite": {
                "description": "礼儀正しく丁寧な性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 1.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 5.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 4, "new_count": 6 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
            },
            "selfish": {
                "description": "自己利益優先的な性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 5.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 1.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 1, "new_count": 9 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(100 / x * 0.7) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(100 / x * 0.7) for x in range(1, n+1)],
            },
            "nervous": {
                "description": "神経質で臆病な性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 2.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 5.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 3, "new_count": 7 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(100 / x * 0.9) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
            },
            "sensitive": {
                "description": "繊細で傷つきやすい性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 1.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 10.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 2, "new_count": 8 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(100 / x * 0.8) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
            },
            "jealous": {
                "description": "嫉妬しやすい性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 3.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 2.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 1, "new_count": 9 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(100 / x * 0.9) for x in range(1, n+1)],
            },
            "talkative": {
                "description": "おしゃべりで口数が多い性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 6.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 6.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 5, "new_count": 5 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(100 / x * 0.9) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
            },
            "entertaining": {
                "description": "人を楽しませるような面白い性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 10.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 10.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 5, "new_count": 5 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(100 / x * 0.9) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
            },
            "evilchildish": {
                "description": "意地悪で子供っぽい性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 20.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 20.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 0, "new_count": 10 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
            },
            "lazyloose": {
                "description": "怠惰でだらしない性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 25.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 25.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 6, "new_count": 12 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
            },
            "unique": {
                "description": "とても変わった例えようのない珍しい性格",
                # 職業P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_occupation": 30.0,
                # 趣味P用重み付け率 1.0 - 58.0(max skills count) 大きいほど緩やかで差が無くなる。
                "weighting_rate_for_interest": 30.0,
                # 趣味Pのスキル取得基本数（ポイントMAXにより増える可能性あり）
                "number_of_interest_choices": { "duplicate_count": 4, "new_count": 17 },
                # 職業Pのスキル分配率関数
                "skill_distribution_rate_function_for_occupation": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
                # 趣味Pのスキル分配率関数
                "skill_distribution_rate_function_for_interest": lambda n: [math.ceil(x / 1.8) for x in range(1, n+1)],
            },
        }

        self.personality_key = None

    def set_key(self, key: str):
        self.personality_key = key

    def get_key(self) -> str:
        return self.personality_key

    def get_description(self) -> str:
        return self.personalitys[self.personality_key]["description"]

    def get_weighting_rate_for_occupation(self) -> int:
        return self.personalitys[self.personality_key]["weighting_rate_for_occupation"]

    def get_weighting_rate_for_interest(self) -> int:
        return self.personalitys[self.personality_key]["weighting_rate_for_interest"]

    def get_number_of_interest_choices(self) -> Dict[str, int]:
        return self.personalitys[self.personality_key]["number_of_interest_choices"]

    def get_skill_distribution_rate_function_for_occupation(self) -> Callable[[int], List[int]]:
        return self.personalitys[self.personality_key]["skill_distribution_rate_function_for_occupation"]

    def get_skill_distribution_rate_function_for_interest(self) -> Callable[[int], List[int]]:
        return self.personalitys[self.personality_key]["skill_distribution_rate_function_for_interest"]

