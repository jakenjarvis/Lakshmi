#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from contents.character.Investigator import Investigator

class AbstractCharacterGetter(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def get_site_title(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def is_detect_url(self, site_url: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def get_favicon_url(self) -> str:
        pass

    @classmethod
    @abstractmethod
    async def request(self, site_url: str) -> Investigator:
        pass
