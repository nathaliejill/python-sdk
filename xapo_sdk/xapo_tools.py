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
import xapo_utils


class MicroPaymentConfig:
    """ Micro payment button configuration options.

    This class is intended to be a placeholder for micro payments
    buttons configuration but also serves for documenting. A dictionary
    with the intended fields would give the same results.

    Attributes:
        sender_user_id (str): The id of the user sending the payment.
        sender_user_email (str, optional): The email of the user sending
            the payment.
        sender_user_cellphone (str, optional): The celphone number of the user
            sending the payment.
        receiver_user_id (str): The id of the user receiving the payment.
        receiver_user_email (str): The email of the user receiving the payment.
        pay_object_id (str): A payment identifier in the TPA context.
        amount_BIT (float, optional): The amount of bitcoins to be payed by the
            widget. If not specified here, it must be entered on payment basis.
        pay_type (str): The string representing the type of operation
            ("Tip", "Pay", "Deposit" or "Donate").
    """
    def __init__(self, sender_user_id="", sender_user_email="",
                 sender_user_cellphone="", receiver_user_id="",
                 receiver_user_email="", pay_object_id="", amount_BIT=0,
                 timestamp=int(round(time.time() * 1000)), pay_type=""):
        self.sender_user_id = sender_user_id
        self.sender_user_email = sender_user_email
        self.sender_user_cellphone = sender_user_cellphone
        self.receiver_user_id = receiver_user_id
        self.receiver_user_email = receiver_user_email
        self.pay_object_id = pay_object_id
        self.amount_BIT = amount_BIT
        self.timestamp = timestamp
        self.pay_type = pay_type


class MicroPayment:
    """ Xapo's payment buttons snippet builder.

    This class allows the construction of 2 kind of widgets, *div* and
    *iframe*. The result is a HTML snippet that could be embedded in a
    web page for doing micro payments though a payment button.

    Attributes:
        service_url: The endpoint URL that returns the payment widget.
        app_id: The id of the TPA for which the widget will be created.
        app_secret: The TPA secret used to encrypt widget configuration.
    """

    def __init__(self, service_url, app_id, app_secret):
        self.service_url = service_url
        self.app_id = app_id
        self.app_secret = app_secret

    def __build_url(self, config):
        json_config = json.dumps(config.__dict__)
        encrypted_config = xapo_utils.encrypt(json_config, self.app_secret)

        query = {"app_id": self.app_id, "button_request": encrypted_config,
                 "customization": json.dumps({"button_text": config.pay_type})}
        query_str = urlencode(query)

        widget_url = self.service_url + "?" + query_str

        return widget_url

    def build_iframe_widget(self, config):
        """ Build an iframe HTML snippet in order to be embedded in apps.

        Args:
            config (MicroPaymentConfig): The button configuration options.
                See @MicroPaymentConfig.

        Returns:
            string: the iframe HTML snippet ot be embedded in a page.

        Example:
        >>> xmp = MicroPayment(
        ... "http://dev.xapo.com:8089/pay_button/show",
        ... "b91014cc28c94841",
        ... "c533a6e606fb62ccb13e8baf8a95cbdc")
        >>> mpc = MicroPaymentConfig(
        ... sender_user_email="sender@xapo.com",
        ... sender_user_cellphone="+5491112341234",
        ... receiver_user_id="r0210",
        ... receiver_user_email="fernando.taboada@xapo.com",
        ... pay_object_id="to0210",
        ... amount_BIT=0.01,
        ... pay_type = "Tip")
        >>> iframe = xmp.build_iframe_widget(mpc)
        >>> print(iframe) # doctest: +ELLIPSIS
        <BLANKLINE>
        <iframe...</iframe>
        <BLANKLINE>
        """
        widget_url = self.__build_url(config)
        snippet = """
                <iframe id="tipButtonFrame" scrolling="no" frameborder="0"
                    style="border:none; overflow:hidden; height:22px;"
                    allowTransparency="true" src="{url}">
                </iframe>
              """.format(url=widget_url)

        return textwrap.dedent(snippet)

    def build_div_widget(self, config):
        """ Build div HTML snippet in order to be embedded in apps.

        Args:
            config (MicroPaymentConfig): The button configuration options.
                See @MicroPaymentConfig.

        Returns:
            string: the div HTML snippet ot be embedded in a page.

        Example:
        >>> xmp = MicroPayment(
        ... "http://dev.xapo.com:8089/pay_button/show",
        ... "b91014cc28c94841",
        ... "c533a6e606fb62ccb13e8baf8a95cbdc")
        >>> mpc = MicroPaymentConfig(
        ... sender_user_email="sender@xapo.com",
        ... sender_user_cellphone="+5491112341234",
        ... receiver_user_id="r0210",
        ... receiver_user_email="fernando.taboada@xapo.com",
        ... pay_object_id="to0210",
        ... amount_BIT=0.01,
        ... pay_type = "Donate")
        >>> div = xmp.build_div_widget(mpc)
        >>> print(div) # doctest: +ELLIPSIS
        <BLANKLINE>
        <div id="tipButtonDiv" class="tipButtonDiv"></div>
        <div id="tipButtonPopup" class="tipButtonPopup"></div>
        <script>...</script>
        <BLANKLINE>
        """
        widget_url = self.__build_url(config)
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

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
