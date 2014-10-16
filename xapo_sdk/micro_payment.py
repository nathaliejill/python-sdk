#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

from future.standard_library import hooks
with hooks():
    from urllib.parse import urlencode

import time
import base64
import textwrap
import json
from Crypto.Cipher import AES


def _pkcs7_encode(bytestring, k=16):
    """
    Pad an input bytestring according to PKCS#7.

    Args:
        bytestring (str): The text to encode.
        k (int, optional): The padding block size. It defaults to k=16.

    Returns:
        str: The padded bytestring.
    """
    l = len(bytestring)
    val = k - (l % k)
    return bytestring + bytearray([val] * val).decode()


# TODO probably this should be moved to xapo_utils.py in order to be
#      reused when the SDK and tools grow up.
def _encrypt(payload, app_secret):
    """ Payload encrypting function.

    Pad and encrypt the payload in order to call XAPO Bitcoin API.

    Args:
        payload (str): The payload to be encrypted.
        app_secret (str): The key used to encrypt the payload.

    Returns:
        str: A string with the encrypted and base64 encoded payload.
    """
    cipher = AES.new(key=app_secret, mode=AES.MODE_ECB)
    padded_payload = _pkcs7_encode(payload)
    encrypted_payload = cipher.encrypt(padded_payload)
    encoded_payload = base64.b64encode(encrypted_payload)

    return encoded_payload


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
    """
    def __init__(self, sender_user_id="", sender_user_email="",
                 sender_user_cellphone="", receiver_user_id="",
                 receiver_user_email="", pay_object_id="", amount_BIT=0,
                 timestamp=int(round(time.time() * 1000))):
        self.sender_user_id = sender_user_id
        self.sender_user_email = sender_user_email
        self.sender_user_cellphone = sender_user_cellphone
        self.receiver_user_id = receiver_user_id
        self.receiver_user_email = receiver_user_email
        self.pay_object_id = pay_object_id
        self.amount_BIT = amount_BIT
        self.timestamp = timestamp


class XapoMicroPaymentSDK:
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

    def __build_url(self, config, pay_type):
        json_config = json.dumps(config.__dict__)
        encrypted_config = _encrypt(json_config, self.app_secret)

        query = {"app_id": self.app_id, "button_request": encrypted_config,
                 "customization": json.dumps({"button_text": pay_type})}
        query_str = urlencode(query)

        widget_url = self.service_url + "?" + query_str

        return widget_url

    def build_iframe_widget(self, config, pay_type):
        """ Build an iframe HTML snippet in order to be embedded in apps.

        Args:
            config (MicroPaymentConfig): The button configuration options.
                See @MicroPaymentConfig.
            pay_type (str): The string representing the type of operation
                      ("Tip", "Pay", "Deposit" or "Donate").

        Returns:
            string: the iframe HTML snippet ot be embedded in a page.

        Example:
        >>> xmp = XapoMicroPaymentSDK(
        ... "http://dev.xapo.com:8089/pay_button/show",
        ... "b91014cc28c94841",
        ... "c533a6e606fb62ccb13e8baf8a95cbdc")
        >>> mpc = MicroPaymentConfig(
        ... sender_user_email="sender@xapo.com",
        ... sender_user_cellphone="+5491112341234",
        ... receiver_user_id="r0210",
        ... receiver_user_email="fernando.taboada@xapo.com",
        ... pay_object_id="to0210",
        ... amount_BIT=0.01)
        >>> iframe = xmp.build_iframe_widget(mpc, pay_type = "Tip")
        >>> print(iframe) # doctest: +ELLIPSIS
        <BLANKLINE>
        <iframe...</iframe>
        <BLANKLINE>
        """
        # TODO see if pay_type should be handled like this, in PHP it's part
        #      of the "request". In this implementation we decoupled the
        #      request from the config object for grater flexibility
        widget_url = self.__build_url(config, pay_type)
        res = """
                <iframe id="tipButtonFrame" scrolling="no" frameborder="0"
                    style="border:none; overflow:hidden; height:22px;"
                    allowTransparency="true" src="{}">
                </iframe>
              """.format(widget_url)

        return textwrap.dedent(res)

    def build_div_widget(self, config, pay_type):
        """ Build div HTML snippet in order to be embedded in apps.

        Args:
            config (MicroPaymentConfig): The button configuration options.
                See @MicroPaymentConfig.
            pay_type (str): The string representing the type of operation
                      ("Tip", "Pay", "Deposit" or "Donate").

        Returns:
            string: the div HTML snippet ot be embedded in a page.

        Example:
        >>> xmp = XapoMicroPaymentSDK(
        ... "http://dev.xapo.com:8089/pay_button/show",
        ... "b91014cc28c94841",
        ... "c533a6e606fb62ccb13e8baf8a95cbdc")
        >>> mpc = MicroPaymentConfig(
        ... sender_user_email="sender@xapo.com",
        ... sender_user_cellphone="+5491112341234",
        ... receiver_user_id="r0210",
        ... receiver_user_email="fernando.taboada@xapo.com",
        ... pay_object_id="to0210",
        ... amount_BIT=0.01)
        >>> div = xmp.build_div_widget(mpc, pay_type = "Tip")
        >>> print(div) # doctest: +ELLIPSIS
        <BLANKLINE>
        <div id="tipButtonDiv" class="tipButtonDiv"></div>
        <div id="tipButtonPopup" class="tipButtonPopup"></div>
        <script>...</script>
        <BLANKLINE>
        """
        widget_url = self.__build_url(config, pay_type)
        res = r"""
                <div id="tipButtonDiv" class="tipButtonDiv"></div>
                <div id="tipButtonPopup" class="tipButtonPopup"></div>
                <script>
                    $(document).ready(function() {{
                        $("#tipButtonDiv").load("{url}");
                    }});
                </script>
              """.format(url=widget_url)

        return textwrap.dedent(res)

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
