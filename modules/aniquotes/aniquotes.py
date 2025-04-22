#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 13:47:01 2025

@author: Luraminaki
"""

import time
import mmap
import inspect
import pathlib
import random
import linecache
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

random.seed(int(time.time()))

CWD = pathlib.Path.cwd()
AQ_FILE = CWD/"data/aniquotes/AQ.txt"


class AniQuotes:
    def __init__(self, aq_file: pathlib.Path=None) -> None:
        self.aq_file = aq_file if aq_file is not None else AQ_FILE
        self.nbr_lines: int = 0

        if self.aq_file.is_file():
            with self.aq_file.open('r+') as aqf:
                buf = mmap.mmap(aqf.fileno(), 0)

                while buf.readline():
                    self.nbr_lines += 1


    def get_random_quote_from_txt(self) -> list[str]:
        curr_func = inspect.currentframe().f_code.co_name

        if not self.nbr_lines:
            logger.warning(f"{curr_func} -- File {self.aq_file.name} is either empty of not loaded")
            return []

        return linecache.getline(str(self.aq_file.absolute()),
                                 random.randint(0, self.nbr_lines)).split('	')