#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple
import re
import math
import random

import LakshmiErrors

class ParameterComplementary():
    OCCUPATIONS = [
        "doctor_of_medicine", "engineer", "entertainer", "professor",
        "zealot", "military_officer", "policeman", "police_detective",
        "artist", "antiquarian", "author", "journalist",
        "private_investigator", "spokesperson", "athlete", "clergyman",
        "parapsychologist", "dilettante", "missionary", "tribal_member",
        "farmer_forester", "pilot", "hacker_consultant", "criminal",
        "soldier", "lawyer", "drifter", "musician",
    ]

    GENDER_DICT = {
        "male" : "男",
        "female" : "女"
    }

    def __init__(self):
        self.gender: str = self.generate_gender()
        self.age: int = self.generate_age()
        self.occupation: str = self.generate_occupation()
        self.sex = self.get_sex()

    def set(self, *, gender: str=None, age: int=None, occupation: str=None):
        if gender is not None:
            if not str(gender).lower() is ParameterComplementary.GENDER_DICT.keys():
                raise LakshmiErrors.ArgumentOutOfRangeException
            self.gender = str(gender).lower()
            self.sex = self.get_sex()

        if age is not None:
            if (age <= 11) or (age > 100):
                raise LakshmiErrors.ArgumentOutOfRangeException
            self.age = int(age)

        if occupation is not None:
            self.occupation = str(occupation)

    def generate_gender(self):
        return random.choice(list(ParameterComplementary.GENDER_DICT.keys()))

    def generate_age(self):
        # これだと高齢者ばかり生まれるので、ちょっと工夫する。かなり適当。
        #result = random.randint(12, 100)
        result = random.randint(18, 35) # とりあえず適齢期

        if random.randint(1, 100) <= 5:
            # クリティカルなら範囲を若くする。
            result = random.randint(12, 25)

        elif random.randint(1, 100) >= 50:
            # 50%の確率で高齢化コース
            result = random.randint(30, 45)
            if random.randint(1, 100) >= 50:
                result = random.randint(40, 55)
                if random.randint(1, 100) >= 40:
                    result = random.randint(50, 65)
                    if random.randint(1, 100) >= 40:
                        result = random.randint(60, 100)
        return result

    def generate_occupation(self):
        return random.choice(ParameterComplementary.OCCUPATIONS)

    def get_sex(self):
        return ParameterComplementary.GENDER_DICT[self.gender]

