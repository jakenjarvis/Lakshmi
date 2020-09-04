#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from contents.Investigator import Investigator

class AbstractCharacterGetter(metaclass=ABCMeta):
    @abstractmethod
    def request(self, site_url: str) -> Investigator:
        pass

    @abstractmethod
    def get(self, unique_key: str) -> Investigator:
        pass

    @abstractmethod
    def register(self, character: Investigator):
        pass
