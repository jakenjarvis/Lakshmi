#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from LakshmiErrors import UnsupportedSitesException
from contents.character.Investigator import Investigator
from contents.character.AbstractCharacterGetter import AbstractCharacterGetter
from contents.character.CharacterVampireBloodNetGetter import CharacterVampireBloodNetGetter

class CharacterGetter():
    def __init__(self):
        self.instances: List[AbstractCharacterGetter] = []
        # 対応サイトの追加
        self.instances.append(CharacterVampireBloodNetGetter())

    def get_target_instance(self, site_url: str) -> AbstractCharacterGetter:
        result = None
        for instance in self.instances:
            if instance.is_detect_url(site_url):
                result = instance
                break
        return result

    def request(self, instance: Investigator, site_url: str) -> bool:
        target_instance = self.get_target_instance(site_url)
        if not target_instance:
            raise UnsupportedSitesException()
        return target_instance.request(instance, site_url)

    def get(self, unique_key: str) -> Investigator:
        pass

    def register(self, character: Investigator):
        pass
