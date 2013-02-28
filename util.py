#!/usr/bin/env python
#-*-encoding:utf-8-*-

import hashlib

def encrypt_password(password,ts):

    token = 'whyalwaysme'
    return hashlib.md5(ts+password+token).hexdigest()


def main():
    import time
    ts = time.time()
    password = '123456'
    res = encrypt_password(password,str(ts))
    print res

if __name__ == "__main__":
    main()

