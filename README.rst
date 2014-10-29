===============================
Xapo SDK & Tools
===============================

.. image:: https://badge.fury.io/py/xapo_sdk.png
    :target: http://badge.fury.io/py/xapo_sdk

.. image:: https://travis-ci.org/frepond/xapo_sdk.png?branch=master
        :target: https://travis-ci.org/frepond/xapo_sdk

.. image:: https://pypip.in/d/xapo_sdk/badge.png
        :target: https://pypi.python.org/pypi/xapo_sdk


Xapo's bitcoin sdk & tools

This is the Python version of the Xapo's Widget Tools. These tools allow you (Third Party Application, TPA) to easily embed tools like Payments Buttons, Donation Buttons and other kind of widgets as DIV or iFrame into your web application using your language of choice. In this way, tedious details like encryption and HTML snippet generation are handled for you in a simple and transparent way.


* Free software: BSD license
* Documentation: https://xapo_sdk.readthedocs.org.


Features
--------

* *Iframe* and *Div* HTML widgets snippet generator.


Micro Payment Widgets
---------------------

Micro payment widgets allow to dynamically get a HTML snippet pre-configured and insert into your web page. Micro payment widgets provides 4 kind of pre-configured actions *Pay, Donate, Tip* and *Deposit*. The widgets allow the following configurations:

- **Amount BIT:** ``[optional]`` sets a fixed amount for the intended payment.
- **Sender's Id:** ``[optional]`` any identifier used in the TPA context to identify the sender.
- **Sender's email:** ``[optional]`` used to pre-load the widget with the user's email.
- **Sender's cellphone:** ``[optional]`` used to pre-load the widget with the user's cellphone.
- **Receiver's Id:** ``[mandatory]`` any receiver's user unique identifier in the TPA context. 
- **Receiver's email:** ``[mandatory]`` the email of the user receiving the payment. It allows XAPO to contact the receiver to claim her payment.
- **Pay Object's Id:** ``[mandatory]`` any unique identifier in the context of the TPA distinguishing the object of the payment.
- **Pay type:** ``[optional]` any of Donate | Pay | Tip | Deposit.