#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals
import base64
from Crypto.Cipher import AES


def _pkcs7_padding(bytestring, k=16):
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


def encrypt(payload, app_secret):
    """ Payload encrypting function.

    Pad and encrypt the payload in order to call XAPO Bitcoin API.

    Args:
        payload (str): The payload to be encrypted.
        app_secret (str): The key used to encrypt the payload.

    Returns:
        str: A string with the encrypted and base64 encoded payload.

    Example:
    >>> json = '{"sender_user_id":"s160901",\
    ... "sender_user_email":"fernando.taboada@gmail.com",\
    ... "sender_user_cellphone":"",\
    ... "receiver_user_id":"r160901"\
    ... "receiver_user_email":"fernando.taboada@xapo.com",\
    ... "tip_object_id":"to160901",\
    ... "amount_SAT":"",\
    ... "timestamp":1410973639125}'
    >>> enc = encrypt(json, "bc4e142dc053407b0028accffc289c18")
    >>> print(enc.decode())
    rjiFHpE3794U23dEKNyEzwd+xx4/r7Lm2W/KcLbRbore5X6QUVCZAkZXCzkbFXNZ+muss+QioH\
Tzf8lVs6TTECU37/2Gqc5CyAmFzN32CoQUBD8mreaOHRu4+UftuMX2Fy6iKlPGHuyxUM+zb0DT8xHe\
k2w5ROtkZJG59A8Vs9xdDEvy3rmDRa56tB/xy2JsjyiT3RtDSDr0+bMfG1mUYNvAymH0aaweJTAJTl\
z0V2/EaArbeee+XHthf7dhXJmktP52nDLXHSDLzr4jCr9uNI6w7EXQ4FR/qRxgu5ieNJ5bZ0YVEKg1\
ax5nikt3hq3zK6pU7eM/VEjAKAAoomlV8uO/WZ6M7kvZaTHd4a7Q9feEGMK3K2zC0I92ArOIPOOa5/\
kRseUtNYNupcZfGBTY0O9njpv3d36BB+nCbPV4ZHg=
    """
    cipher = AES.new(key=app_secret, mode=AES.MODE_ECB)
    padded_payload = _pkcs7_padding(payload)
    encrypted_payload = cipher.encrypt(padded_payload)
    encoded_payload = base64.b64encode(encrypted_payload)

    return encoded_payload

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
