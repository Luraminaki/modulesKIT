#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 13:47:01 2025

@author: Luraminaki
"""

import inspect
import logging

from fastapi import APIRouter

from modules.helpers import statics

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GenericViews:
    def __init__(self, module_name: str, *args, **kwargs) -> None:
        self.module_name: str = module_name

        self.api_router = APIRouter(prefix=f"/api/{module_name}", tags=["API"])
        self.api_router.add_api_route("/url-list", self.get_all_urls, methods=['GET'])


    async def get_all_urls(self) -> dict[str, str |
                                              list |
                                              list[dict[str, str | list[str]]] |
                                              list[dict[str, dict]]]:
        curr_func = inspect.currentframe().f_code.co_name

        try:
            data = [{'path': route.path,
                     'name': route.name,
                     'description': route.description,
                     'methods': list(route.methods),
                     'query_params': [{'name': query_param.name,
                                       'core_schema': getattr(query_param._type_adapter, 'core_schema', {})}
                                      for query_param in getattr(route.dependant, 'query_params', [])],
                     'response_model': [str(response_model)
                                        for response_model in route.response_model
                                        if route.response_model]}
                    for route in self.api_router.routes
                    if route.name != 'get_all_urls']
        except Exception as err:
            logger.error(f"{curr_func} -- {repr(err)}")
            return {'status': statics.StatusFunction.ERROR.name, 'error': repr(err)}

        return {'status': statics.StatusFunction.SUCCESS.name, 'data': data, 'error': ''}
