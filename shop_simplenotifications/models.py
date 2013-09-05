#-*- coding: utf-8 -*-
"""Signal handlers for shop_simplenotifications."""
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, RequestContext

from shop.order_signals import confirmed


def subject(template_name):
    """Returns the email subject based on the subject template."""
    subject = loader.render_to_string(template_name,
                                      self.get_context())
    return ''.join(subject.splitlines())

def confirmed_email_notification(sender, **kwargs):
    """
    Sends an email notification to the shop owner when a new order is
    completed.
    """
    subject_template_name = 'shop_simplenotifications/confirmed_subject.txt'
    body_template_name = 'shop_simplenotifications/confirmed_body.txt'
    request = kwargs.get('request')
    order = kwargs.get('order')
    subject = loader.render_to_string(
        subject_template_name,
        RequestContext(request, {'order': order})
    )
    subject = subject.join(subject.splitlines())
    body = loader.render_to_string(
        body_template_name,
        RequestContext(request, {'order': order})
    )
    from_email = getattr(settings, 'SN_FROM_EMAIL',
                         settings.DEFAULT_FROM_EMAIL)
    owners = getattr(settings, 'SN_OWNERS', settings.ADMINS)
    send_mail(subject, body, from_email,
              [owner[1] for owner in owners], fail_silently=False)

confirmed.connect(confirmed_email_notification)


def payment_instructions_email_notification(sender, **kwargs):
    """
    Sends an email with payment instructions to the customer once and order is
    placed.
    """
    subject_template_name = \
            'shop_simplenotifications/payment_instructions_subject.txt'
    body_template_name = \
            'shop_simplenotifications/payment_instructions_body.txt'
    request = kwargs.get('request')
    order = kwargs.get('order')
    if order.user and order.user.email:
        subject = loader.render_to_string(
            subject_template_name,
            RequestContext(request, {'order': order})
        )
        subject = subject.join(subject.splitlines())
        body = loader.render_to_string(
            body_template_name,
            RequestContext(request, {'order': order})
        )
        from_email = getattr(settings, 'SN_FROM_EMAIL',
                             settings.DEFAULT_FROM_EMAIL)
        send_mail(subject, body, from_email,
                  [order.user.email,], fail_silently=False)

confirmed.connect(payment_instructions_email_notification)

