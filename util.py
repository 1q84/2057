#!/usr/bin/env python
#-*-encoding:utf-8-*-

import hashlib
import types

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

def main():
    import time
    ts = time.time()
    password = '123456'
    res = encrypt_password(password,str(ts))
    print res

if __name__ == "__main__":
    main()

