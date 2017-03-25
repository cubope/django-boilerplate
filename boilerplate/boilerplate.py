# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

# Default settings
BOILERPLATE_DEFAULTS = {
    'model_url_list_suffix': '_list',
    'app_url_index': 'home',
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
