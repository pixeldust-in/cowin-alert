from typing import NamedTuple

from django.conf import settings
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Attachment(NamedTuple):  # noqa
    name: str = ""
    data: bytes = b""
    content_type: str = ""


def send_mass_individual_mail(  # noqa
    recipient_list,
    subject: str,
    context,
    template: str,
    from_email: str = settings.DEFAULT_FROM_EMAIL,
    attachments: list[Attachment] = list(),
):
    """
    A convinience function to send mails using a template to a bunch of
    recipients individually(for datatuples use send_mail_tuples below)
    but by using a single connection to the server.

    The function uses EmailMultiAlternatives to send both plain text and
    text/html versions and attachments. It differs from
    django.core.mail.send_mass_mail in that there is no data tuple, each
    recipient is sent mail separately, message is rendered first and you
    have the option of sending attachment/s.
    """
    html_content = render_to_string(template, context)
    text_content = strip_tags(html_content)
    messages = []
    for recipient in recipient_list:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
        msg.attach_alternative(html_content, "text/html")
        if attachments:
            for attachment in attachments:
                msg.attach(attachment.name, attachment.data, attachment.content_type)
        messages.append(msg)
    connection = mail.get_connection()
    return connection.send_messages(messages)


def send_mail_tuples(datatuple):
    """
    Given a datatuple of (subject, html_content, from_email, recipient_list, attachments), send
    each message to each recipient list. Return the number of emails sent.

    If from_email is None, use the DEFAULT_FROM_EMAIL setting.
    If attachments skip adding any attachments

    Differs from the django.core.mail.send_mass_mail in the sense that it defaults to sending
    html mails with attachments. The default implementation is just for simple text mails. While
    this one has better shennanigans for your pure and unbriddled html pleasure.

    """
    messages = []
    for subject, html_content, from_email, recipient_list, attachments in datatuple:
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        if attachments and len(attachments) > 0:
            for attachment in attachments:
                msg.attach(attachment.name, attachment.data, attachment.content_type)
        messages.append(msg)
    connection = mail.get_connection()
    return connection.send_messages(messages)
