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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.helpers.generic_api_views import GenericViews

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CWD = pathlib.Path.cwd()
CONFIG_FILE = CWD/"config.json"


def generic_create_app(config: dict, module_views: GenericViews=None) -> FastAPI:
    curr_func = inspect.currentframe().f_code.co_name

    if module_views is None:
        raise ValueError(f"{curr_func} -- module_views is None")

    webapp = FastAPI(title=module_views.module_name,
                     description=config['modules'][module_views.module_name].get('description', ''),
                     version=config['version'])

    webapp.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # MUST be in that specific order, else it doesn't work
    webapp.include_router(module_views.api_router)

    return webapp


def generic_main(main: callable=None, version: str=''):
    curr_func = inspect.currentframe().f_code.co_name
    m_tic = time.perf_counter()

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configuration', help='Configuration file location', required=False)
    args = vars(parser.parse_args())

    config_file = args.get('configuration', None)
    if config_file is None:
        config_file = CONFIG_FILE
    else:
        config_file = pathlib.Path(config_file)

    if not config_file.is_file():
        logger.error(f"{curr_func} -- {config_file} does not exist -- Aborting")
        sys.exit(1)

    try:
        with config_file.open('r', encoding='utf-8') as f:
            conf: dict = json.load(f)
            conf['version'] = version

    except Exception as err:
        logger.error(f"{curr_func} -- Loading {config_file} failed -- {repr(err)}")
        sys.exit(1)

    logger.info(f"{curr_func} -- Current time is: {time.asctime(time.localtime())}")
    logger.info(f"{curr_func} -- {config_file} acquired")

    ret_val: int = main(conf)

    m_tac = time.perf_counter() - m_tic
    logger.info(f"{curr_func} -- Ellapsed time: {round(m_tac, 3)}")

    sys.exit(ret_val)
