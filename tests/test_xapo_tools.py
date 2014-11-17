#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_xapo_tools
----------------------------------

Tests for `xapo_tools` module.
"""

import unittest2

from xapo_sdk import xapo_tools
from xapo_sdk.xapo_tools import PaymentType
import re

TEST = False


# TODO set your credentials ans TEST to True
@unittest2.skipIf(not TEST, "Set your credentials and TEST to True")
class TestXapo_tools(unittest2.TestCase):

    def setUp(self):
        self.mp = xapo_tools.MicroPayment(
            "https://mpayment.xapo.com/pay_button/show"
            "your app id",
            "your app secret")
        self.mp_notpa = xapo_tools.MicroPayment(
            "https://mpayment.xapo.com/pay_button/show")

    def test_build_iframe_widget(self):
        config = xapo_tools.MicroPaymentConfig(
            sender_user_email="sender@xapo.com",
            sender_user_cellphone="+5491112341234",
            receiver_user_id="r0210",
            receiver_user_email="fernando.taboada@xapo.com",
            pay_object_id="to0210",
            amount_BIT=1,
            pay_type=PaymentType.TIP,
            end_mpayment_uri="http://localhost:9000",
            redirect_uri="http://localhost:9000")
        customization = xapo_tools.MicroPaymentCustomization(
            login_cellphone_header_title="Test MicroPayment",
            predefined_pay_values="1,5,10",
            button_css="red")

        iframe = self.mp.build_iframe_widget(config, customization)
        regex = r'\n<iframe(.*)button_request(.*)>(.*)</iframe>\n'

        print(iframe)
        self.assertNotEqual(None,
                            re.match(regex, iframe, re.MULTILINE | re.DOTALL))

    def test_build_iframe_widget_notpa(self):
        config = xapo_tools.MicroPaymentConfig(
            sender_user_email="sender@xapo.com",
            sender_user_cellphone="+5491112341234",
            receiver_user_id="r0210",
            receiver_user_email="fernando.taboada@xapo.com",
            pay_object_id="to0210",
            amount_BIT=0.01,
            pay_type=PaymentType.TIP,
            end_mpayment_uri="http://localhost:9000",
            redirect_uri="http://localhost:9000")
        customization = xapo_tools.MicroPaymentCustomization(
            login_cellphone_header_title="Test MicroPayment",
            predefined_pay_values="1,5,10",
            button_css="grey")

        iframe = self.mp_notpa.build_iframe_widget(config, customization)
        regex = r'\n<iframe(.*)payload(.*)>(.*)</iframe>\n'

        print(iframe)
        self.assertNotEqual(None,
                            re.match(regex, iframe, re.MULTILINE | re.DOTALL))

    def test_build_div_widget(self):
        config = xapo_tools.MicroPaymentConfig(
            sender_user_email="sender@xapo.com",
            sender_user_cellphone="+5491112341234",
            receiver_user_id="r0210",
            receiver_user_email="fernando.taboada@xapo.com",
            pay_object_id="to0210",
            amount_BIT=0.01,
            pay_type=PaymentType.DONATE,
            end_mpayment_uri="http://localhost:9000",
            redirect_uri="http://localhost:9000")
        customization = xapo_tools.MicroPaymentCustomization(
            login_cellphone_header_title="Test MicroPayment",
            predefined_pay_values="1,5,10",
            button_css="red")

        div = self.mp.build_div_widget(config, customization)
        regex = r"""
<div id="tipButtonDiv" class="tipButtonDiv"></div>
<div id="tipButtonPopup" class="tipButtonPopup"></div>
<script>(.*)button_request(.*)</script>
"""
        print(div)
        self.assertNotEqual(None,
                            re.match(regex, div, re.MULTILINE | re.DOTALL))

    def test_build_div_widget_notpa(self):
        config = xapo_tools.MicroPaymentConfig(
            sender_user_email="sender@xapo.com",
            sender_user_cellphone="+5491112341234",
            receiver_user_id="r0210",
            receiver_user_email="fernando.taboada@xapo.com",
            pay_object_id="to0210",
            amount_BIT=0.01,
            pay_type=xapo_tools.PaymentType.DONATE,
            end_mpayment_uri="http://localhost:9000",
            redirect_uri="http://localhost:9000")
        customization = xapo_tools.MicroPaymentCustomization(
            login_cellphone_header_title="Test MicroPayment",
            predefined_pay_values="1,5,10",
            button_css="grey")

        div = self.mp_notpa.build_div_widget(config, customization)
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
