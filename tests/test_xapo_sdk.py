#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_xapo_sdk
----------------------------------

Tests for `xapo_sdk` module.
"""

import unittest

from xapo_sdk import xapo_utils
from xapo_sdk import xapo_tools
import re


class TestXapo_sdk(unittest.TestCase):

    def setUp(self):
        self.mp = xapo_tools.MicroPayment(
            "http://dev.xapo.com:8089/pay_button/show",
            "b91014cc28c94841",
            "c533a6e606fb62ccb13e8baf8a95cbdc")
        self.mp_notpa = xapo_tools.MicroPayment(
            "http://dev.xapo.com:8089/pay_button/show")

    def test_encrypt(self):
        json = """{"sender_user_id":"s160901",\
"sender_user_email":"fernando.taboada@gmail.com",\
"sender_user_cellphone":"",\
"receiver_user_id":"r160901"\
"receiver_user_email":"fernando.taboada@xapo.com",\
"tip_object_id":"to160901",\
"amount_SAT":"",\
"timestamp":1410973639125}"""
        enc = xapo_utils.encrypt(json, "bc4e142dc053407b0028accffc289c18")
        expected = b'rjiFHpE3794U23dEKNyEz3ukF5rhVxtKzxEnZq8opuHoRH5eA/XOEbROE\
zf5AYmyQ5Yw6cQLSVMx/JgENrNKVK268n3o1kOIxEpupaha2wYXLqIqU8Ye7LFQz7N\
vQNPzfyOSPWnBQ/JUCSKsCiCz45VoK511B/RMz33mjJMF7s2qkQlCjukzZ1rry5gRF\
XaOxGgK23nnvlx7YX+3YVyZpLT+dpwy1x0gy86+Iwq/bjSh/V65R9Og71Zm47MjxKr\
scoJWV5+pzlSKKx2bTCqBX1sI+gedozC1GEdKINy9Ug67XvtqyXMjKBlxZIC4vTw9q\
gjV/sbkB7LZ2ShWFIBJRQ=='

        print(json)
        print(enc.decode())
        self.assertEquals(expected, enc)

    def test_build_iframe_widget(self):
        mpc = xapo_tools.MicroPaymentConfig(
            sender_user_email="sender@xapo.com",
            sender_user_cellphone="+5491112341234",
            receiver_user_id="r0210",
            receiver_user_email="fernando.taboada@xapo.com",
            pay_object_id="to0210",
            amount_BIT=0.01,
            pay_type="Tip")
        iframe = self.mp.build_iframe_widget(mpc)
        regex = r'\n<iframe(.*)button_request(.*)>(.*)</iframe>\n'

        print(iframe)
        self.assertNotEqual(None,
                            re.match(regex, iframe, re.MULTILINE | re.DOTALL))

    def test_build_iframe_widget_notpa(self):
        mpc = xapo_tools.MicroPaymentConfig(
            sender_user_email="sender@xapo.com",
            sender_user_cellphone="+5491112341234",
            receiver_user_id="r0210",
            receiver_user_email="fernando.taboada@xapo.com",
            pay_object_id="to0210",
            amount_BIT=0.01,
            pay_type="Tip")
        iframe = self.mp_notpa.build_iframe_widget(mpc)
        regex = r'\n<iframe(.*)payload(.*)>(.*)</iframe>\n'

        print(iframe)
        self.assertNotEqual(None,
                            re.match(regex, iframe, re.MULTILINE | re.DOTALL))

    def test_build_div_widget(self):
        mpc = xapo_tools.MicroPaymentConfig(
            sender_user_email="sender@xapo.com",
            sender_user_cellphone="+5491112341234",
            receiver_user_id="r0210",
            receiver_user_email="fernando.taboada@xapo.com",
            pay_object_id="to0210",
            amount_BIT=0.01,
            pay_type="Donate")
        div = self.mp.build_div_widget(mpc)
        regex = r"""
<div id="tipButtonDiv" class="tipButtonDiv"></div>
<div id="tipButtonPopup" class="tipButtonPopup"></div>
<script>(.*)button_request(.*)</script>
"""
        print(div)
        self.assertNotEqual(None, 
                            re.match(regex, div, re.MULTILINE | re.DOTALL))

    def test_build_div_widget_notpa(self):
        mpc = xapo_tools.MicroPaymentConfig(
            sender_user_email="sender@xapo.com",
            sender_user_cellphone="+5491112341234",
            receiver_user_id="r0210",
            receiver_user_email="fernando.taboada@xapo.com",
            pay_object_id="to0210",
            amount_BIT=0.01,
            pay_type="Donate")
        div = self.mp_notpa.build_div_widget(mpc)
        regex = r"""
<div id="tipButtonDiv" class="tipButtonDiv"></div>
<div id="tipButtonPopup" class="tipButtonPopup"></div>
<script>(.*)payload(.*)</script>
"""

        print(div)
        self.assertNotEqual(None, 
                            re.match(regex, div, re.MULTILINE | re.DOTALL))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
