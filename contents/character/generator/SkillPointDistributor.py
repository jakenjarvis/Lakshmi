#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple
import math
import random
import copy
from collections import OrderedDict

class SkillPointDistributor():
    def __init__(self, skills: List[str], probabilitys: List[int], current_values: List[int]):
        self.original_skills: List[str] = skills
        self.current_values: List[int] = current_values

        self.skills: List[str] = copy.deepcopy(skills)
        self.probabilitys: List[float] = copy.deepcopy(probabilitys)
        print(self.probabilitys)

        if not (len(self.skills) == len(self.probabilitys) == len(self.current_values)):
            raise IndexError

        self.result_hangar = OrderedDict()
        for skill in self.skills:
            self.result_hangar[skill] = 0

    def __choice(self, target: List[str], weights: List[int]) -> str:
        return random.choices(target, weights=weights, k=1)[0]

    def lottery(self, points: int):
        # 効率悪いけど、１ポイントずつ抽選しながら割り振る。
        for count in range(points):
            pick = self.__choice(self.skills, self.probabilitys)
            pick_index = self.skills.index(pick)
            original_index = self.original_skills.index(pick)

            self.result_hangar[pick] += 1
            current_value = self.current_values[original_index]

            # スキル最大値の85に到達したら、該当スキルを抽選リストから除外する。
            if (current_value + self.result_hangar[pick]) >= 85:
                del self.skills[pick_index]
                del self.probabilitys[pick_index]

    def get_value(self, skill: str) -> int:
        return self.result_hangar[skill]
