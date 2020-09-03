#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from contents.Character import Character

class AbstractCharacterGetter(metaclass=ABCMeta):
    @abstractmethod
    def request(self, site_url: str) -> Character:
        pass

    @abstractmethod
    def get(self, unique_key: str) -> Character:
        pass

    @abstractmethod
    def register(self, character: Character):
        pass
