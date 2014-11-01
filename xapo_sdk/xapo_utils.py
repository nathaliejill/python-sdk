#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals
import base64
from Crypto.Cipher import AES


def _pkcs7_padding(bytestring, k=16):
    """ Pad an input bytestring according to PKCS#7.

    Args:
        bytestring (str): The text to encode.

        k (int, optional): The padding block size. It defaults to k=16.

    Returns:
        str: The padded bytestring.
    """
    l = len(bytestring)
    val = k - (l % k)
    return bytestring + bytearray([val] * val).decode()


def encrypt(payload, app_secret):
    """ Payload encrypting function.

    Pad and encrypt the payload in order to call XAPO Bitcoin API.

    Args:
        payload (str): The payload to be encrypted.

        app_secret (str): The key used to encrypt the payload.

    Returns:
        str: A string with the encrypted and base64 encoded payload.
    """
    cipher = AES.new(key=app_secret, mode=AES.MODE_ECB)
    padded_payload = _pkcs7_padding(payload)
    encrypted_payload = cipher.encrypt(padded_payload)
    encoded_payload = base64.b64encode(encrypted_payload)

    return encoded_payload
