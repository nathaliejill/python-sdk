========
Usage
========

To use Xapo SDK & Tools in a project::

    import xapo_sdk

---------------------
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
- **Pay type:** ``[optional]`` any of Donate | Pay | Tip | Deposit.


^^^^^^^^^^^^^
IFrame Widget
^^^^^^^^^^^^^

.. code:: python

    xmp = MicroPayment(
        "http://dev.xapo.com:8089/pay_button/show",
        "b91014cc28c94841",
        "c533a6e606fb62ccb13e8baf8a95cbdc")
    mpc = MicroPaymentConfig(
        sender_user_email="sender@xapo.com",
        sender_user_cellphone="+5491112341234",
        receiver_user_id="r0210",
        receiver_user_email="fernando.taboada@xapo.com",
        pay_object_id="to0210",
        amount_BIT=0.01,
        pay_type = "Tip")
    iframe = xmp.build_iframe_widget(mpc)  

    print(iframe) 


With this you get the following snippet:

.. code:: html

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

^^^^^^^^^^
Div Widget
^^^^^^^^^^

.. code:: python

    from xapo_sdk import xapo_tools

    xmp = xapo_tools.MicroPayment(
        "http://dev.xapo.com:8089/pay_button/show",
        "b91014cc28c94841",
        "c533a6e606fb62ccb13e8baf8a95cbdc")
    mpc = xapo_tools.MicroPaymentConfig(
        sender_user_email="sender@xapo.com",
        sender_user_cellphone="+5491112341234",
        receiver_user_id="r0210",
        receiver_user_email="fernando.taboada@xapo.com",
        pay_object_id="to0210",
        amount_BIT=0.01,
        pay_type = "Donate")
    div = xmp.build_div_widget(mpc)

    print(div)


With this you get the following snippet:

.. code:: html

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

^^^^^^^^^^^^^^^
Widgets Gallery
^^^^^^^^^^^^^^^

.. _a link: http://developers.xapo.com/images/payment_widget/donate_button.png

.. _a link: http://developers.xapo.com/images/payment_widget/mpayment1.png

.. _a link: http://developers.xapo.com/images/payment_widget/mpayment2.png

.. _a link: http://developers.xapo.com/images/payment_widget/mpayment3.png