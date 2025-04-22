#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 13:47:01 2025

@author: Luraminaki
"""

import enum


class StatusFunction(enum.Enum):
    SUCCESS = enum.auto()
    FAIL = enum.auto()
    ONGOING = enum.auto()
    DONE = enum.auto()
    ERROR = enum.auto()
    WARNING = enum.auto()
