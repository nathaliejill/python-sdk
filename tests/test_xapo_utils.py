#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_xapo_utils
----------------------------------

Tests for `xapo_utils` module.
"""

import unittest

from xapo_sdk import xapo_utils


class TestXapo_utils(unittest.TestCase):
    def setUp(self):
        pass

    def test_encrypt(self):
        json = """{"sender_user_id":"s160901",\
"sender_user_email":"fernando.taboada@gmail.com",\
"sender_user_cellphone":"",\
"receiver_user_id":"r160901"\
"receiver_user_email":"fernando.taboada@xapo.com",\
"tip_object_id":"to160901",\
"amount_SAT":"",\
"timestamp":1410973639125}"""
        enc = xapo_utils.encrypt(json, "bc4e142dc053407b0028accffc289c18",
                                 xapo_utils.pkcs7_padding)
        expected = b'rjiFHpE3794U23dEKNyEz3ukF5rhVxtKzxEnZq8opuHoRH5eA/XOEbROE\
zf5AYmyQ5Yw6cQLSVMx/JgENrNKVK268n3o1kOIxEpupaha2wYXLqIqU8Ye7LFQz7N\
vQNPzfyOSPWnBQ/JUCSKsCiCz45VoK511B/RMz33mjJMF7s2qkQlCjukzZ1rry5gRF\
XaOxGgK23nnvlx7YX+3YVyZpLT+dpwy1x0gy86+Iwq/bjSh/V65R9Og71Zm47MjxKr\
scoJWV5+pzlSKKx2bTCqBX1sI+gedozC1GEdKINy9Ug67XvtqyXMjKBlxZIC4vTw9q\
gjV/sbkB7LZ2ShWFIBJRQ=='

        print(json)
        print(enc.decode())
        self.assertEquals(expected, enc)
