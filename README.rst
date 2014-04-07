django-shop-simplenotifications
================================

Only use this, if you are brave!

This is a dead simple approach on email notifications for django-shop. The
goal of this app is to hook into django-shop's various signals in order to 
send emails to the shop owner and to the buyer on certain events.

Installation
=============

Install this package into your virtualenv::

  pip install django-shop-simplenotifications 

Add the app to your INSTALLED_APPS setting::

  INSTALLED_APPS = (
      ...
      'shop_simplenotifications',
  )

Configuration
==============

SN_FROM_EMAIL
++++++++++++++

Default: DEFAULT_FROM_EMAIL

The from address for your automated emails. Example::

  SN_EMAIL_FROM = 'noreply@myshop.com'

SN_OWNERS
++++++++++

Default: ADMINS

A tuple that lists people who get notifications about new incoming orders and
payments. Each member of the tuple should be a tuple of
(Full name, email address). Example::

  (('John', 'john@example.com'), ('Mary', 'mary@example.com'))

Templates
==========

In order to easily provide notifications with the wording and formatting of
your choice, there are templates for all email subjects and bodies. In order
to override the defaults, add the folowing templates to your
``templates/shop_simplenotifications/`` folder:

  * confirmed_subject.txt
  * confirmed_body.txt
  * payment_instructions_subject.txt
  * payment_instructions_body.txt

You have the option of providing html versions of `confirmed_body.txt` and
`payment_instructions_body.txt` (in addition to the .txt files), which will be
sent as an alternative content type for email clients that render html.

All templates have a ``request`` and an ``order`` variable in their context. 

Please note that the sender in the PaymentBackend should pass the ``request`` as well. 
Example::

  confirmed.send(sender=self, order=order, request=request)


Features
=========

  * When a buyer completes his order, the shop owners get a notification mail
  * When a buyer requests prepayment, the shop owners get a notification mail 
    and the buyer gets the payment instructions. The email address will be taken from 
		a) the logged in User, if available and/or 
		b) the billing address, 
	if available and the address model has an ``email`` attribute. If both address 
	are equal, only one email will be sent. This works for guests and logged in 
	Users. 
  * All notification emails can be easily templated.

Testing
========

If you want to contribute to this project and quickly need to run the
test-suite, you need to do the following steps:

  * create a virtual environment
  * fork this repository
  * install this package into your virtual environment
  * manually install the django-shop dependency (this step will be gone soon)
  * execute ``runtests.py``

Example::

  mkvirtualenv -p python2.7 yourenvname
  workon yourenvname
  git clone git://github.com/bitmazk/django-shop-simplenotifications.git
  cd django-shop-simplenotifications
  python setup.py install
  pip install -e git+git://github.com/divio/django-shop.git#egg=shop
  cd shop_simplenotifications/tests
  ./runtests.py
