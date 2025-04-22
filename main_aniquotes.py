#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 13:47:01 2025

@author: Luraminaki
"""

import sys
import time
import json
import inspect
import pathlib
import argparse
import logging
import logreset

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

#pylint: disable=no-name-in-module
from __ver__ import __version__
#pylint: enable=no-name-in-module

from modules.aniquotes import api_views

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CWD = pathlib.Path.cwd()
CONFIG_FILE = CWD/"config.json"

APP_NAME = 'aniquotes'


def create_app(config: dict, app_name: str,):
    webapp = FastAPI(title=app_name, description=config['modules'][app_name].get('description', ''), version=__version__)

    webapp.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # MUST be in that specific order, else it doesn't work
    module_views = api_views.AniQuotesView(module_name=app_name,
                                           modules_config=config)
    webapp.include_router(module_views.api_router)

    return webapp


if __name__ == "__main__":
    c_func = inspect.currentframe().f_code.co_name
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

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configuration', help='Configuration file location', required=False)
    args = vars(parser.parse_args())

    config_file = args.get('configuration', None)
    if config_file is None:
        config_file = CONFIG_FILE
    else:
        config_file = pathlib.Path(config_file)

    if not config_file.is_file():
        logger.error(f"{c_func} -- {config_file} does not exist -- Aborting")
        sys.exit(1)

    try:
        with config_file.open('r', encoding='utf-8') as f:
            conf: dict = json.load(f)
    except Exception as err:
        logger.error(f"{c_func} -- Loading {config_file} failed -- {repr(err)}")
        sys.exit(1)

    logger.info(f"{c_func} -- Current time is: {time.asctime(time.localtime())}")
    logger.info(f"{c_func} -- {config_file} acquired")
    crash = False

    try:
        app = create_app(conf, APP_NAME)
        uvicorn.run(app,
                    port=conf['modules'][APP_NAME]['port'],
                    log_config=log_config)
    except Exception as err:
        crash = True
        logger.error(f"{c_func} -- App chrashed at {time.asctime(time.localtime())} -- {repr(err)}")

    m_tac = time.perf_counter() - m_tic
    logger.info(f"{c_func} -- Ellapsed time: {round(m_tac, 3)}")

    if crash:
        sys.exit(1)

    sys.exit(0)

# fastapi dev main_aniquotes.py
