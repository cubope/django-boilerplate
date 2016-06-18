# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from importlib import import_module

# Default settings
BOILERPLATE_DEFAULTS = {
	'site_name': '',
	'messages': {
		'change_password_current': _('You can\'t use your old password. Type a new password.'),
		'change_password_new': _('Passwords don\'t match.'),
		'login_credentials': _('Wrong username or password. Please try again.'),
		'login_inactive': _('Your account has been deactivated. Please contact the site adminitrator.'),
		'recover_unknown': _('We couldn\'t find your username or email.'),
		'registration_email': _('Email missmatch.'),
		'registration_password': _('Password missmatch.'),
		'registration_username_already': _('Username already taken.'),
		'registration_email_already': _('Another account has that email.'),
		'recover_sent': _('An email has been sent to %(email)s. Please check its inbox to continue reseting password.'),
		'recover_subject': _('[%s] Recover your account information'),
	}
}

# Start with a copy of default settings
BOILERPLATE = BOILERPLATE_DEFAULTS.copy()

# Override with user settings from settings.py
BOILERPLATE.update(getattr(settings, 'BOILERPLATE', {}))

def get_boilerplate_setting(setting, default=None):
	"""
	Read a setting
	"""
	return BOILERPLATE.get(setting, default)

def messages(**kwargs):
	"""
	Return the dict with the messages
	"""
	return get_boilerplate_setting('messages')

def site_name(**kwargs):
	"""
	Return the the full site_name
	"""
	return get_boilerplate_setting('site_name')

def recover_url_name(**kwargs):
	"""
	Return the the full recover_url_name
	"""
	return get_boilerplate_setting('recover_url_name')