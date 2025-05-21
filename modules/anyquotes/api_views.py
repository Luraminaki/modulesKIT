#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 13:47:01 2025

@author: Luraminaki
"""

import inspect
import logging

from modules.helpers import statics
from modules.helpers import generic_api_views
from modules.anyquotes import anyquotes

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QuotesView(generic_api_views.GenericViews):
    def __init__(self, modules_config: dict | None = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.aq = anyquotes.AnyQuotes(self.module_name, modules_config)
        self.api_router.add_api_route("/quote",
                                      self.get_quote,
                                      methods=['GET'],
                                      description=f"Picks a random quote from the {', '.join(file.stem for file in self.aq.q_datas)} file(s) available")


    async def get_quote(self) -> dict[str, str]:
        curr_func = (cf.f_code.co_name
                     if (cf := inspect.currentframe()) is not None
                     else 'None')

        try:
            if not(res := self.aq.get_random_quote_from_csv()):
                return {'status': statics.StatusFunction.ERROR.name, 'error': ''}

        except Exception as err:
            logger.error(f"{curr_func} -- {repr(err)}")
            return {'status': statics.StatusFunction.ERROR.name, 'error': repr(err)}

        return {'status': statics.StatusFunction.SUCCESS.name, 'data': res, 'error': ''}
