#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from contents.Investigator import Investigator

class AbstractCharacterGetter(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def detect_url(self, site_url: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def request(self, site_url: str) -> Investigator:
        pass
