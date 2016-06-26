# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def add_view_permissions(sender, **kwargs):
	for content_type in ContentType.objects.all():
		codename = "view_%s" % content_type.model

		if not Permission.objects.filter(content_type=content_type, codename=codename):
			Permission.objects.create(content_type=content_type,
				codename=codename,
				name='Can view %s' % content_type.name)
			print 'Added view permission for %s' % content_type.name