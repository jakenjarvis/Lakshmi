#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple
import math
import random
import copy
from collections import OrderedDict

class GeneratedSubSkill():
    def __init__(self):
        self.subskills = {
            "own_language": [
                "日本語",
            ],
            "other_language": [
                "英語",
                "ラテン語",
                "中国語",
                "韓国語",
                "朝鮮語",
                "ヒンディー語",
                "エジプト語",
                "スペイン語",
                "イタリア語",
                "アラビア語",
                "ポルトガル語",
                "ロシア語",
                "フランス語",
                "ドイツ語",
                "ベトナム語",
                "ベンガル語",
                "ジャワ語",
                "トルコ語",
                "ポーランド語",
                "ペルシア語",
                "タイ語",
                "ウクライナ語",
            ],
            "drive": [
                "原動機付自転車",
                "普通自動車",
                "普通二輪車",
                "大型二輪車",
                "大型二輪車",
                "準中型自動車",
                "中型自動車",
                "大型自動車",
                "小型特殊自動車",
                "大型特殊自動車",
            ],
            "craft": [
                "料理",
                "装飾",
                "衣装",
                "製本",
                "陶芸",
                "彫刻",
                "アロマ",
                "菓子",
                "民芸品",
                "執筆",
                "漫画",
                "絵画",
                "楽器",
                "大工",
                "石工",
                "鉄工",
            ],
            "pilot": [
                "特殊小型船舶",
                "小型船舶",
                "大型船舶",
                "自家用飛行機",
                "事業用飛行機",
                "准定期運送用飛行機",
                "定期運送用飛行機",
            ],
            "art": [
                "料理",
                "歌唱",
                "演舞",
                "ダンス",
                "社交ダンス",
                "演劇",
                "絵画",
                "陶芸",
                "装飾",
                "執筆",
                "文学",
                "書道",
                "漫画",
                "古書",
                "民芸品",
                "鍵盤楽器",
                "管楽器",
                "弦楽器",
                "打楽器",
                "骨董品",
                "古物",
                "建築設計",
            ],
        }

    def is_subkey(self, key: str):
        return (key in self.subskills)

    def choice(self, key: str) -> str:
        # 上位ほど選ばれやすくする。
        target = self.subskills[key]
        weights = [math.ceil(100 / x ** 2.0) for x in range(1, len(target)+1)]
        result = random.choices(target, weights=weights, k=1)[0]
        return result
