#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 13:47:01 2025

@author: Luraminaki
"""

import sys
import time
import inspect
import pathlib
import logging
import logreset

from fastapi import FastAPI
import uvicorn

#pylint: disable=no-name-in-module
from __ver__ import __version__
#pylint: enable=no-name-in-module

from modules.helpers.generic_app import generic_main, generic_create_app
from modules.anyquotes import api_views

APP_NAME = pathlib.Path(__file__).stem.replace('main_', '')

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)


def create_app(config: dict, app_name: str) -> FastAPI:
    return generic_create_app(config,
                              api_views.QuotesView(module_name=app_name,
                                                   modules_config=config))


def main(conf: dict) -> int:
    curr_func = (cf.f_code.co_name
                 if (cf := inspect.currentframe()) is not None
                 else 'None')

    try:
        logger.info(f"{curr_func} -- Creating APP: {APP_NAME}")
        app = create_app(conf, APP_NAME)
        uvicorn.run(app,
                    port=conf['modules'][APP_NAME]['port'],
                    log_config=log_config)
        return 0

    except Exception as err:
        logger.error(f"{curr_func} -- App chrashed at {time.asctime(time.localtime())} -- {repr(err)}")
        return 1


if __name__ == "__main__":
    c_func = (cf.f_code.co_name
              if (cf := inspect.currentframe()) is not None
              else 'None')
    m_tic = time.perf_counter()

    logreset.reset_logging()

    level = logging.INFO
    log_config = logging.basicConfig(
        level=level,
            format="[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s",
            handlers=[
                logging.FileHandler(f'./logs/{pathlib.Path(__file__).stem}.log', mode='w', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    logger.setLevel(level)

    logger.info(f"{c_func} -- Version {__version__}")

    generic_main(main, __version__)

# fastapi dev main_anyquotes.py
