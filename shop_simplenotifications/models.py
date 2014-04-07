#-*- coding: utf-8 -*-
"""Signal handlers for shop_simplenotifications."""
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template import loader, RequestContext, TemplateDoesNotExist

from shop.order_signals import confirmed
from shop.util.address import get_billing_address_from_request

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
    body_text_template_name = 'shop_simplenotifications/confirmed_body.txt'
    body_html_template_name = 'shop_simplenotifications/confirmed_body.html'
    request = kwargs.get('request')
    order = kwargs.get('order')
    subject = loader.render_to_string(
        subject_template_name,
        RequestContext(request, {'order': order})
    )
    subject = subject.join(subject.splitlines())

    text_content = loader.render_to_string(
        body_text_template_name,
        RequestContext(request, {'order': order})
    )
    try:
        html_content = loader.render_to_string(
            body_html_template_name,
            RequestContext(request, {'order': order})
        )
    except TemplateDoesNotExist:
        html_content = None

    from_email = getattr(settings, 'SN_FROM_EMAIL',
                         settings.DEFAULT_FROM_EMAIL)
    owners = getattr(settings, 'SN_OWNERS', settings.ADMINS)

    message = EmailMultiAlternatives(subject, text_content, from_email,
                                     [owner[1] for owner in owners])
    if html_content:
        message.attach_alternative(html_content, "text/html")
    message.send()

confirmed.connect(confirmed_email_notification)


def payment_instructions_email_notification(sender, **kwargs):
    """
    Sends an email with payment instructions to the customer once and order is
    placed.
    """
    subject_template_name = \
            'shop_simplenotifications/payment_instructions_subject.txt'
    body_text_template_name = \
            'shop_simplenotifications/payment_instructions_body.txt'
    body_html_template_name = \
            'shop_simplenotifications/payment_instructions_body.html'
    
    request = kwargs.get('request')
    order = kwargs.get('order')
    
    emails = []
    if order.user and order.user.email: 
        emails.append(order.user.email)
    if request and get_billing_address_from_request(request):
        address = get_billing_address_from_request(request)
        if hasattr(address, 'email'):
            emails.append(address.email)
        emails.append(address.email)

    emails = list(set(emails)) # removes duplicated entries
    if emails:
        subject = loader.render_to_string(
            subject_template_name,
            RequestContext(request, {'order': order})
        )
        subject = subject.join(subject.splitlines())

        text_content = loader.render_to_string(
            body_text_template_name,
            RequestContext(request, {'order': order})
        )

        try:
            html_content = loader.render_to_string(
                body_html_template_name,
                RequestContext(request, {'order': order})
            )
        except TemplateDoesNotExist:
            html_content = None

        from_email = getattr(settings, 'SN_FROM_EMAIL',
                             settings.DEFAULT_FROM_EMAIL)

        message = EmailMultiAlternatives(subject, text_content, from_email,
                                         emails)
        if html_content:
            message.attach_alternative(html_content, "text/html")
        message.send()

confirmed.connect(payment_instructions_email_notification)

