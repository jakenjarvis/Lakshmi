#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from discord.ext.commands.errors import CommandError

class PermissionNotFoundException(Exception):
    pass

class ArgumentOutOfRangeException(CommandError):
    pass

class SubcommandNotFoundException(CommandError):
    pass

class UnsupportedSitesException(CommandError):
    pass

class CharacterNotFoundException(CommandError):
    pass
