#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_xapo_api
----------------------------------

Tests for `xapo_api` module.
"""

import unittest2

import uuid
from xapo_sdk import xapo_api

TEST = False


# TODO set your credentials ans TEST to True
@unittest2.skipIf(not TEST, "Set your credentials and TEST to True")
class TestXapo_tools(unittest2.TestCase):
    def setUp(self):
        self.api = xapo_api.API('https://api.xapo.com/v1',
                                'your app id',
                                'your app secret')

    def test_credit(self):
        res = self.api.credit(to='sample@xapo.com', amount=1,
                              currency=xapo_api.Currency.SAT,
                              comments='Sample deposit',
                              request_id=uuid.uuid1().hex)

        print(res)

        self.assertTrue(res['success'])
        self.assertEquals('Success', res['code'])

    def test_credit_bad_amount(self):
        res = self.api.credit(to='sample@xapo.com', amount=-0.5,
                              comments='Sample deposit',
                              request_id=uuid.uuid1().hex)

        print(res)

        self.assertFalse(res['success'])
        self.assertEquals('InvalidAmount', res['code'])

    def test_credit_missing_to(self):
        res = self.api.credit(to='', amount=0.5,
                              comments='Sample deposit',
                              request_id=uuid.uuid1().hex)

        print(res)

        self.assertFalse(res['success'])
        self.assertEquals('Failure', res['code'])
