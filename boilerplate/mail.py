# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils import translation

def send_raw_mail(user, template_prefix, subject, object=None, from_name=None, files=None):
	"""
	Sending emails is easy now.

	**Example**
	::
		send_raw_mail(<User:user>, 'recover_password', 'Recover Password', {'url': XXX})
	"""
	if isinstance(user, User):
		if hasattr(user, 'profile'):
			translation.activate(user.profile.language)
		to_email = user.email
	else:
		to_email = user

	if not from_name:
		from_name = settings.DEFAULT_FROM_EMAIL

	from_email = settings.DEFAULT_FROM_EMAIL

	if object:
		context = {'object': object}
	else:
		context = {}

	template_plain = get_template('mail/' + template_prefix + '.txt')
	text_content   = template_plain.render(context)
	msg            = EmailMultiAlternatives(subject, text_content, '%s <%s>' % (from_name, from_email), [to_email, ])

	if files:
		for name, file, content_type in files:
			msg.attach(name, file.read(), content_type)

	return msg.send()

def send_html_mail(user, template_prefix, subject, object=None, from_name=None, files=None):
	"""
	Sending html emails is easy now.

	**Example**
	::
		send_html_mail(<User:user>, 'recover_password', 'Recover Password', {'url': XXX})
	"""
	if isinstance(user, User):
		if hasattr(user, 'profile'):
			translation.activate(user.profile.language)
		to_email = user.email
	else:
		to_email = user

	if not from_name:
		from_name = settings.DEFAULT_FROM_EMAIL

	from_email = settings.DEFAULT_FROM_EMAIL

	if object:
		context = {'object': object}
	else:
		context = {}

	template_plain = get_template('mail/' + template_prefix + '.txt')
	template_html  = get_template('mail/' + template_prefix + '.html')
	text_content   = template_plain.render(context)
	html_content   = template_html.render(context)
	msg            = EmailMultiAlternatives(subject, text_content, '%s <%s>' % (from_name, from_email), [to_email, ])
	msg.attach_alternative(html_content, 'text/html')

	if files:
		for name, file, content_type in files:
			msg.attach(name, file.read(), content_type)

	return msg.send()