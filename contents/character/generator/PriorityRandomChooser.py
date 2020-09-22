#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple
import math
import random
import copy
from collections import OrderedDict

class PriorityRandomChooser():
    def __init__(self, items: List[any]=None):
        # コピーを操作する。
        if items is None:
            self.priority_list: List[any] = []
        else:
            self.priority_list: List[any] = copy.deepcopy(items)

        self.narrow_list: List[any] = []

    def __choice(self, target_list: List[any]) -> any:
        # 引数のリストから公平に選択する。
        result = random.choice(target_list)
        # 削除するのは、管理リストから
        self.chosen(result)
        return result

    def __choice_by_priority_weighting_rate(self, target_list: List[any], rate: float) -> any:
        # 引数のリストから上位の物を優先的に選択する。
        weights = list(reversed([math.ceil(_ / rate) for _ in range(1, len(target_list)+1)]))
        result = random.choices(target_list, weights=weights, k=1)[0]
        # 削除するのは、管理リストから
        self.chosen(result)
        return result

    def __create_new_priority_list(self, narrow_list: List[any]) -> List[any]:
        result = []
        new_index_list = []
        for target in narrow_list:
            index = self.priority_list.index(target)
            new_index_list.append((index, target))
        new_index_list = sorted(new_index_list, key=lambda x: x[0])

        for target in new_index_list:
            result.append(target[1])
        return result

    def is_choose_for_narrowing_down(self):
        return ((len(self.priority_list) >= 1) and (len(self.narrow_list) >= 1))

    def chosen(self, item: any):
        # 削除するのは、管理リストから
        self.priority_list.remove(item)
        return self

    def choice(self) -> any:
        return self.__choice(self.priority_list)

    def choice_by_priority_weighting_rate(self, rate: float) -> any:
        return self.__choice_by_priority_weighting_rate(self.priority_list, rate)

    def narrowing_down_chosen(self, item: any):
        # 削除するのは、narrow_listから
        self.narrow_list.remove(item)
        return self

    def set_narrowing_down_conditions(self, narrow_list: List[any]=None):
        if narrow_list is None:
            self.narrow_list = []
        else:
            self.narrow_list = self.__create_new_priority_list(copy.deepcopy(narrow_list))

    def narrowing_down_choice(self) -> any:
        new_list = self.__create_new_priority_list(self.narrow_list)
        result = self.__choice(new_list)
        self.narrowing_down_chosen(result)
        return result

    def narrowing_down_choice_by_priority_weighting_rate(self, rate: float) -> any:
        new_list = self.__create_new_priority_list(self.narrow_list)
        result = self.__choice_by_priority_weighting_rate(new_list, rate)
        self.narrowing_down_chosen(result)
        return result

    def chosen_all_narrowing_down_conditions(self):
        for target in self.narrow_list:
            self.chosen(target)
        self.narrow_list = []
        return self
