# -*- coding: utf-8 -*-
import sys

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def add_view_permissions(sender, **kwargs):
    """
    Create a view permission for all the models in an specific app

    **Example**
    ::
    # File: apps.py
    from django.db.models.signals import post_migrate
    from boilerplate.signals import add_view_permissions

    class MyAppConfig(AppConfig):
        ...

        def ready(self):
            post_migrate.connect(add_view_permissions, sender=self)
    ::
    """
    for content_type in ContentType.objects.filter(app_label=sender.label):
        codename = "view_%s" % content_type.model

        perm, created = Permission.objects.get_or_create(
            content_type=content_type, codename=codename, defaults={
                'name': 'Can view %s' % content_type.name,
            }
        )

        if created:
            sys.stdout.write(
                'Added view permission for %s' % content_type.name +
                '\n'
            )
