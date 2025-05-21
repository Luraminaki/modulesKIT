#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 13:47:01 2025

@author: Luraminaki
"""

import csv
import time
import mmap
import inspect
import pathlib
import random
import linecache
import logging
import unidecode

from typing import Generator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

random.seed(int(time.time()))

CWD = pathlib.Path.cwd()


class AnyQuotes:
    def __init__(self, module_name: str | None = None,
                 modules_config: dict | None = None) -> None:
        if (not modules_config
            or not module_name
            or modules_config is None
            or module_name is None):
            raise ValueError(f"{self.__class__.__name__} -- Invalid module_name configuration file provided -- {module_name} : {modules_config}")

        self.module_name: str = module_name
        self.module_datas: dict[str, str] = modules_config['modules'][self.module_name]['datas']

        data_path: pathlib.Path = pathlib.Path(modules_config['directories']['data_directory'])/self.module_name
        input_files: Generator[pathlib.Path] = data_path.glob('*.csv', case_sensitive=False)
        self.q_datas: dict[pathlib.Path,
                           dict[str,
                                int | str | list[str]]] = {file_name: {}
                                                           for file_name in input_files}

        for q_file in self.q_datas:
            nbr_lines: int = 0

            with q_file.open('r+') as qf:
                reader = csv.reader(qf, delimiter=';')
                header = next(reader)

                buf = mmap.mmap(qf.fileno(), 0)

                while buf.readline():
                    nbr_lines += 1

            self.q_datas[q_file] = {'nbr_lines': nbr_lines,
                                    'header': header}


    def pretty_quote(self, source_file: str, data_quote: dict[str, str]) -> str:
        template: str = self.module_datas.get('template', '')
        return (template.replace('<quote>', '\n- '.join(unidecode.unidecode(data_quote['quote']).split(' - ')))
                        .replace('<author>', unidecode.unidecode(data_quote['author']))
                        .replace('<source_file>', unidecode.unidecode(source_file)))


    def get_random_quote_from_csv(self) -> str:
        curr_func = (cf.f_code.co_name
                     if (cf := inspect.currentframe()) is not None
                     else 'None')

        if not self.q_datas:
            logger.warning(f"{curr_func} -- Quote file folder is either empty or failed to be loaded")
            return ''

        q_file, q_details = random.choice(list(self.q_datas.items()))
        q_line: str = (linecache.getline(str(q_file.absolute()),
                                         random.randint(1, q_details['nbr_lines'])).rstrip('\r\n')
                       if isinstance(q_details['nbr_lines'], int)
                       else '')

        q_data: dict[str, str] = ({elem_type.lower(): elem
                                   for elem_type, elem in zip(q_details['header'],
                                                              q_line.split(';'))
                                   if isinstance(elem_type, str) and isinstance(elem, str)}
                                  if isinstance(q_details['header'], list)
                                  else {'quote': 'Nothing wrong with a man taking pleasure in his work.',
                                        'author': 'John Doe'})

        return self.pretty_quote(q_file.stem,
                                 data_quote=q_data)
