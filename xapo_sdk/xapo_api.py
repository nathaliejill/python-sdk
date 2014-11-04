#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import requests
import time
import json

from xapo_sdk import xapo_utils


class Currency:
    BTC = "BTC"
    SAT = "SAT"


class API:
    __service_url = None
    __app_id = None
    __app_secret = None

    __credit_resource = "/credit"

    def __init__(self, service_url, app_id, app_secret):
        self.__service_url = service_url
        self.__app_id = app_id
        self.__app_secret = app_secret

    def credit(self, to, amount, request_id, currency=Currency.BTC,
               comments="", subject=""):
        timestamp = int(round(time.time() * 1000))
        payload = {
            "to": to,
            "currency": currency,
            "amount": amount,
            "comments": comments,
            "subject": subject,
            "timestamp": timestamp,
            "unique_request_id": request_id
        }

        json_payload = json.dumps(payload)
        encrypted_payload = xapo_utils.encrypt(json_payload, self.__app_secret)
        query = {"appID": self.__app_id, "hash": encrypted_payload}

        r = requests.get(url=self.__service_url + self.__credit_resource,
                         params=query)

        return r.json()
