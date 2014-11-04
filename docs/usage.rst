Usage
=====

To use Xapo SDK & Tools in a project::

    import xapo_sdk


API
---
The of the API allows third party application to interact with Xapo wallets and resources in a simple and intuitive way.


Development Environment:

    http://dev.xapo.com/api/v1

Credit
~~~~~~

The Credit API allows any Third Party Application (TPA) to load Bitcoins into any Xapo Wallet using a secure App_ID + App_Shared_Key authentication method.

Parameters
++++++++++

- **To:** ``(string, mandatory)`` any e­mail, BTC address or mobile number.
- **Currency:** ``(Currency, mandatory)`` any of ``Currency.BTC`` or ``Currency.SAT`` .
- **Amount:** ``(numeric, mandatory)`` amount to be credited.
- **Comments:** ``(string, optional)`` note or message to attach to the transaction.
- **Subject:** ``(string, optional)`` if specified, will be used as email subject (when crediting an email address) or SMS text (when crediting a mobile #). 
- **Timestamp:** ``(int, mandatory)`` UTC Unix Timestamp. The request will be rejected if using a timestamp not equal or greater than the last used by previous request.
- **Resquest Id:** ``(string, mandatory)`` any ID that uniquely identifies this request. Cannot be repeated with any new request.    

Result
++++++

The result is a dictionary containing:

======= ======= ===============================================================
Key     Type    Description
======= ======= ===============================================================
success boolean Indicates whether the request was successfully processed or not
code    string  A response code
message string  Description of the result
======= ======= ===============================================================

Error codes:

================= ================================================================
Code              Message
================= ================================================================
Success           Wallet successfully credited
InvalidRequest    Either the App token or Hash are invalid
ExpiredRequest    The request timestamp and/or unique_request_id have expired
InvalidWallet     Wallet not linked with this APP
InvalidEmail      The destination email is invalid
InvalidBTCAddress The destination BTC address is invalid
InvalidCellphone  The destination mobile number is invalid
InvalidCurrency   The currency is invalid
InvalidAmount     The amount to deposit is invalid
MinimumAmount     The amount to deposit must be at least XXX
InsufficientFunds The wallet you are withdrawing from does not have enough available balance to fulfill the Deposit
================= ================================================================

Usage Example
+++++++++++++

.. code:: python

    import uuid
    from xapo_sdk import xapo_api

    ...

    # config the api
    xapo_api.API(SERVICE_URL, APP_ID, APP_SECRET)
   
    ...

    # call cerdit service
    res = api.credit(to='sample@xapo.com', amount=0.5,
                     comments='Sample deposit',
                     request_id=uuid.uuid1().hex)

    print(res)


Micro Payment Widgets
---------------------

Micro payment widgets allow to dynamically get a HTML snippet pre-configured and insert into your web page. Micro payment widgets provides 4 kind of pre-configured actions *Pay, Donate, Tip* and *Deposit*. The widgets allow the following configurations:

- **Amount BIT:** ``(number, optional)`` sets a fixed amount for the intended payment.
- **Sender's Id:** ``(string, optional)`` any identifier used in the TPA context to identify the sender.
- **Sender's email:** ``(string, optional)`` used to pre-load the widget with the user's email.
- **Sender's cellphone:** ``(string, optional)`` used to pre-load the widget with the user's cellphone.
- **Receiver's Id:** ``(string, mandatory)`` any receiver's user unique identifier in the TPA context. 
- **Receiver's email:** ``(string, mandatory)`` the email of the user receiving the payment. It allows XAPO to contact the receiver to claim her payment.
- **Pay Object's Id:** ``(string, mandatory])`` any unique identifier in the context of the TPA distinguishing the object of the payment.
- **Pay type:** ``(string, optional)`` any of Donate | Pay | Tip | Deposit.

Be aware that micro payments could be optionally configured with your own application id and secret (`app_id`/`app_secret`). Configuring the micro payment with your application credentials allows you to charge a transaction fee for example.


Development Environment:

    http://dev.xapo.com:8089/pay_button/show


IFrame Widget
~~~~~~~~~~~~~

.. code:: python

    from xapo_sdk import xapo_tools

    xmp = xapo_tools.MicroPayment(SERVICE_URL, APP_ID, APP_SECRET)
    mpc = xapo_tools.MicroPaymentConfig(
        sender_user_email='sender@xapo.com',
        sender_user_cellphone='+5491112341234',
        receiver_user_id='r0210',
        receiver_user_email='fernando.taboada@xapo.com',
        pay_object_id='to0210',
        amount_BIT=0.01,
        pay_type = 'Tip')
    iframe = xmp.build_iframe_widget(mpc)  

    print(iframe) 


With this you get the following snippet:

.. code::

    <iframe id='tipButtonFrame' scrolling='no' frameborder='0' 
        style='border:none; overflow:hidden; height:22px;' 
        allowTransparency='true' 
        src='http://dev.xapo.com:8089/pay_button/show?customization=%7B
        %22button_text%22%3A%22Tip%22%7D&app_id=b91014cc28c94841&button
        _request=C%2F6OaxS0rh3jMhH90kRYyp3y%2BU5ADcCgMLCyz2P5ssFG%2FJoG
        f55ccvicyRMuIXpU5xhDeHGffpZAvVeMCpJhGFyIPwLFh%2FVdnjnDUjYgJCQeB
        4mCpGsEW5SC6wNvg69ksgeAtr108Wc5miA8H4JG99EWTTlC7WtIGg5rFKkbjrop
        15fSJfhv5cTs02jSC5f2BaLlh1mKh5hSPW3HGcWcl%2BdyZj%2F9m1lPB4gKfky
        2%2FnT0tYjbEFo5aU6WtowWrf2xE8OYejyI0poEFkClBkv2eDkp4Gel4tGb%2Bk
        wszcyb18ztK89RlBwhe8sX4HeM2KJM8ZaWuDOGH2VW4kbThMCZEw%3D%3D'>
    </iframe>

See the example results in the :ref:`widgets-gallery`.


Div Widget
~~~~~~~~~~

.. code:: python

    from xapo_sdk import xapo_tools

    xmp = xapo_tools.MicroPayment((SERVICE_URL, APP_ID, APP_SECRET)
    mpc = xapo_tools.MicroPaymentConfig(
        sender_user_email='sender@xapo.com',
        sender_user_cellphone='+5491112341234',
        receiver_user_id='r0210',
        receiver_user_email='fernando.taboada@xapo.com',
        pay_object_id='to0210',
        amount_BIT=0.01,
        pay_type = 'Donate')
    div = xmp.build_div_widget(mpc)

    print(div)


With this you get the following snippet:

.. code::

    <div id='tipButtonDiv' class='tipButtonDiv'></div>
    <div id='tipButtonPopup' class='tipButtonPopup'></div>
    <script>
    $(document).ready(function() {
        $('#tipButtonDiv').load(
            'http://dev.xapo.com:8089/pay_button/show?
            customization=%7B%22button_text%22%3A%22Donate%22%7D&
            app_id=b91014cc28c94841&button_request=C%2F6OaxS0rh3jMhH90k
            RYyp3y%2BU5ADcCgMLCyz2P5ssFG%2FJoGf55ccvicyRMuIXpU5xhDeHGff
            pZAvVeMCpJhGFyIPwLFh%2FVdnjnDUjYgJCQeB4mCpGsEW5SC6wNvg69ksg
            eAtr108Wc5miA8H4JG99EWTTlC7WtIGg5rFKkbjrop15fSJfhv5cTs02jSC
            5f2BaLlh1mKh5hSPW3HGcWcl%2BdyZj%2F9m1lPB4gKfky2%2FnT0tYjbEF
            o5aU6WtowWrf2xE8OYejyI0poEFkClBkv2eDkp4Gel4tGb%2Bkwszcyb18z
            tK89RlBwhe8sX4HeM2KJMHVfAM8NQXQu8oiIyCAl0vg%3D%3D');
        });
    </script>

See the example results in the :ref:`widgets-gallery`.


.. _widgets-gallery:


Widgets Gallery
~~~~~~~~~~~~~~

.. image:: http://developers.xapo.com/images/payment_widget/donate_button.png

.. image:: http://developers.xapo.com/images/payment_widget/mpayment1.png

.. image:: http://developers.xapo.com/images/payment_widget/mpayment2.png

.. image:: http://developers.xapo.com/images/payment_widget/mpayment3.png