# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

# Default settings
BOILERPLATE_DEFAULTS = {
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
