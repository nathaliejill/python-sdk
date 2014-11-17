#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

from future.standard_library import hooks
with hooks():
    from urllib.parse import urlencode

import time
import textwrap
import json
from xapo_sdk import xapo_utils


class PaymentType:
    NONE = ''
    TIP = 'Tip'
    DEPOSIT = 'Deposit'
    PAY = 'Pay'
    DONATE = 'Donate'
    OAUTH = 'Oauth'


class MicroPaymentConfig:
    """ Micro payment button configuration options.

    This class is intended to be a placeholder for micro payments
    buttons configuration but also serves for documenting. A dictionary
    with the intended fields would give the same results.

    Attributes:
        sender_user_id (str): The id of the user sending the payment.

        sender_user_email (str, optional): The email of the user sending
        the payment.

        sender_user_cellphone (str, optional): The celphone number of the
        user sending the payment.

        receiver_user_id (str): The id of the user receiving the payment.

        receiver_user_email (str): The email of the user receiving the payment.

        pay_object_id (str): A payment identifier in the TPA context.

        amount_BIT (float, optional): The amount of bitcoins to be payed by the
        widget. If not specified here, it must be entered on payment basis.

        pay_type (str): The string representing the type of operation
        ("Tip", "Pay", "Deposit" or "Donate").

        reference_code (str, optional): A custom code to be tracked by the
        TPA. It's sent back to the TPA in the specified callback. It could be
        used also to search with the micro payments query API.

        end_mpayment_uri (str, optional): The callback URL to notify a
        successful micro payment. The callback will be called with parameters
        "reference_code" and "request_UID".

        end_mpayment_redirect_uri (str, optional): An URL to be redirected to
        after a successful micro payment.

        redirect_uri (str, optional): redirect URL after a successful OAuth 
        flow. The URL must accept a "code" parameter if access is granted or
        "error" and "error_description" in case of denial.
    """
    def __init__(self, sender_user_id="", sender_user_email="",
                 sender_user_cellphone="", receiver_user_id="",
                 receiver_user_email="", pay_object_id="", amount_BIT=0,
                 timestamp=int(round(time.time() * 1000)),
                 pay_type=PaymentType.NONE, reference_code="", 
                 end_mpayment_uri="", end_mpayment_redirect_uri="",
                 redirect_uri=""):
        self.sender_user_id = sender_user_id
        self.sender_user_email = sender_user_email
        self.sender_user_cellphone = sender_user_cellphone
        self.receiver_user_id = receiver_user_id
        self.receiver_user_email = receiver_user_email
        self.pay_object_id = pay_object_id
        self.amount_BIT = amount_BIT
        self.timestamp = timestamp
        self.pay_type = pay_type
        self.reference_code = reference_code
        self.end_mpayment_uri = end_mpayment_uri
        self.end_mpayment_redirect_uri = end_mpayment_redirect_uri
        self.redirect_uri = redirect_uri


class MicroPaymentCustomization:
    """ Micro payment button configuration options.

    This function is intended to be a helper for creating empty micro
    payments buttons customization but also serves for documenting. A
    hash with the intended fields would give the same results.

    Attributes:
        login_cellphone_header_title+ (str, optional): Text to appear in the
        login screen. Default: "Support content creators by sending them bits.
        New users receive 50 bits to get started!"

        predefined_pay_values+ (str, optional): A string of comma separated
        amount values, e.g. "1,5,10".

        button_css+ (str, optional): optional CSS button customization
        ("red" | "grey").
    """
    def __init__(self, login_cellphone_header_title="",
                 predefined_pay_values="", button_css=""):
        self.login_cellphone_header_title = login_cellphone_header_title
        self.predefined_pay_values = predefined_pay_values
        self.button_css = button_css


class MicroPayment:
    """ Xapo's payment buttons snippet builder.

    This class allows the construction of 2 kind of widgets, *div* and
    *iframe*. The result is a HTML snippet that could be embedded in a
    web page for doing micro payments though a payment button.

    Attributes:
        service_url (str): The endpoint URL that returns the payment widget.

        app_id (str, optional): The id of the TPA for which the widget will
        be created.

        app_secret (str, optional): The TPA secret used to encrypt widget
        configuration.
    """

    def __init__(self, service_url, app_id=None, app_secret=None):
        self.service_url = service_url
        self.app_id = app_id
        self.app_secret = app_secret

    def __build_url(self, config, customization):
        json_config = json.dumps(config.__dict__)

        if (self.app_id is None or self.app_secret is None):
            query = {
                "payload": json_config,
                "customization": json.dumps(customization.__dict__)
            }
            query_str = urlencode(query)
        else:
            encrypted_config = xapo_utils.encrypt(json_config, self.app_secret,
                                                  xapo_utils.pkcs7_padding)
            query = {
                "app_id": self.app_id,
                "button_request": encrypted_config,
                "customization": json.dumps(customization.__dict__)
            }

        query_str = urlencode(query)
        widget_url = self.service_url + "?" + query_str

        return widget_url

    def build_iframe_widget(self, config, customization):
        """ Build an iframe HTML snippet in order to be embedded in apps.

        Args:
            config (MicroPaymentConfig): The button configuration options.
            See @MicroPaymentConfig.

        Returns:
            str: the iframe HTML snippet ot be embedded in a page.
        """
        widget_url = self.__build_url(config, customization)
        snippet = """
                <iframe id="tipButtonFrame" scrolling="no" frameborder="0"
                    style="border:none; overflow:hidden; height:22px;"
                    allowTransparency="true" src="{url}">
                </iframe>
              """.format(url=widget_url)

        return textwrap.dedent(snippet)

    def build_div_widget(self, config, customization):
        """ Build div HTML snippet in order to be embedded in apps.

        Args:
            config (MicroPaymentConfig): The button configuration options.
            See @MicroPaymentConfig.

        Returns:
            str: the div HTML snippet ot be embedded in a page.
        """
        widget_url = self.__build_url(config, customization)
        snippet = r"""
                <div id="tipButtonDiv" class="tipButtonDiv"></div>
                <div id="tipButtonPopup" class="tipButtonPopup"></div>
                <script>
                    $(document).ready(function() {{
                        $("#tipButtonDiv").load("{url}");
                    }});
                </script>
              """.format(url=widget_url)

        return textwrap.dedent(snippet)
