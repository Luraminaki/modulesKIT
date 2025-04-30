#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 13:47:01 2025

@author: Luraminaki
"""

import inspect
import pathlib
import logging

from modules.helpers import statics
from modules.helpers import generic_api_views
from modules.aniquotes import aniquotes

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QuotesView(generic_api_views.GenericViews):
    def __init__(self, modules_config: dict=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.aq = aniquotes.AniQuotes(pathlib.Path(
            str(modules_config['directories']['data_directory']
                + self.module_name
                + '/'
                + modules_config['modules'][self.module_name]['datas']['aq_file'])
        ))

        self.api_router.add_api_route("/get_aniquote",
                                      self.get_aniquote,
                                      methods=['GET'],
                                      description=f"Picks a random anime quote from the {self.aq.nbr_lines} available")


    async def get_aniquote(self) -> dict[str, str]:
        curr_func = inspect.currentframe().f_code.co_name

        try:
            if not((res := self.aq.get_random_quote_from_txt())
                and (len(res) == 3)):
                return {'status': statics.StatusFunction.ERROR.name, 'error': ''}

        except Exception as err:
            logger.error(f"{curr_func} -- {repr(err)}")
            return {'status': statics.StatusFunction.ERROR.name, 'error': repr(err)}

        anime, character, quote = res
        data: str = f"```{quote}\n-{character}```\n> {anime}"

        return {'status': statics.StatusFunction.SUCCESS.name, 'data': data, 'error': ''}
