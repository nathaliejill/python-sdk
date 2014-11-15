#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_xapo_tools
----------------------------------

Tests for `xapo_tools` module.
"""

import unittest

from xapo_sdk import xapo_tools
from xapo_sdk.xapo_tools import PaymentType
import re


class TestXapo_tools(unittest.TestCase):

    def setUp(self):
        self.mp = xapo_tools.MicroPayment(
            "https://mpayment.xapo.com/pay_button/show",
            "b91014cc28c94841",
            "c533a6e606fb62ccb13e8baf8a95cbdc")
        self.mp_notpa = xapo_tools.MicroPayment(
            "https://mpayment.xapo.com/pay_button/show")

    def test_build_iframe_widget(self):
        mpc = xapo_tools.MicroPaymentConfig(
            sender_user_email="sender@xapo.com",
            sender_user_cellphone="+5491112341234",
            receiver_user_id="r0210",
            receiver_user_email="fernando.taboada@xapo.com",
            pay_object_id="to0210",
            amount_BIT=0.01,
            pay_type=PaymentType.TIP)
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
            pay_type=PaymentType.TIP)
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
            pay_type=PaymentType.DONATE)
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
            pay_type=xapo_tools.PaymentType.DONATE)
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
