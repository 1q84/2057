#!/usr/bin/env python
#-*-encoding:utf-8-*-

import hashlib
import types
import markdown
import re
import time
import os

def mark_down(value):
    strlt = re.compile('<')
    html = strlt.sub( '&lt;',value )
    strbr = re.compile('\r\n')
    html = strbr.sub( '<br/>',html )
    return markdown.markdown(html)

def encrypt_password(password,ts):

    token = 'whyalwaysme'
    return hashlib.md5(ts+password+token).hexdigest()

def valid_normal_params(args):
    try:
        dic = {}
        for k, v in args.items():
            dic[k] = get_first_item(v)
        return True, dic
    except Exception,e:
        return False, None

def get_first_item(item):
    if type(item) is types.NoneType:
        return ''
    elif type(item) is types.ListType:
        if len(item) > 0:
            return item[0]
        else:
            return ''
    elif type(item) is types.StringType:
        return item

def gen_avatar_path():
    ts = int(time.time())
    return str(ts)
    
def enum(**enums):
    return type('Enum', (), enums)

GENDER = enum(MALE=0,FEMALE=1)
NOTIFICATION = enum(COMMENT=0,FANS=1)
