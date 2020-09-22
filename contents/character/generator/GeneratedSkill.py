#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple
import re
import math
import random
import copy
from collections import OrderedDict

from contents.character.generator.GeneratedSubSkill import GeneratedSubSkill

class GeneratedSkill():
    MATCH_SUB_SKILL_NAME = re.compile(r"^([^(]+)[(](.*)[)]$", re.IGNORECASE)

    def __init__(self):
        self.skill_key: str = ""        # キー名
        self.skill_subkey: str = ""     # サブキー名

        self.skill_subname = ""         # サブスキル名

        self.generated_subskill = GeneratedSubSkill()

    def set_definition(self, skill_definition: str):
        match = GeneratedSkill.MATCH_SUB_SKILL_NAME.search(skill_definition)
        if match:
            self.skill_key = str(match.group(1)).strip()
            self.skill_subkey = str(match.group(2)).strip()
        else:
            self.skill_key = str(skill_definition)
            self.skill_subkey = ""

        if self.generated_subskill.is_subkey(self.skill_key):
            if self.skill_subkey == "" or self.skill_subkey == "*":
                self.skill_subname = self.generated_subskill.choice(self.skill_key)
            else:
                self.skill_subname = self.skill_subkey
        return self

    def to_display_string(self):
        result = ""
        if len(self.skill_subkey) >= 1:
            result = f"{self.skill_key}({self.skill_subkey}): {self.skill_subname}"
        else:
            result = f"{self.skill_key}: {self.skill_subname}"
        return result
