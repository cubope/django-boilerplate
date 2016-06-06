# -*- encoding: utf-8 -*-
import unicodedata
from django import template
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
	dict_        = request.GET.copy()
	dict_[field] = value
	return dict_.urlencode()

@register.filter
def get_deleted_objects(object):
	collector = NestedObjects(using=DEFAULT_DB_ALIAS)
	collector.collect([object])
	
	return collector.nested()

"""

Form filters

"""
@register.filter
def form_model_name(value):
	return value._meta.model._meta.verbose_name.title()

@register.filter
def form_model_name_plural(value):
	return value._meta.model._meta.verbose_name_plural.title()

@register.filter
def form_model_url(value):
	return value._meta.model._meta.app_label + ':' + value._meta.model.__name__.lower() + '_list'

@register.filter
def form_app_name(value):
	return value._meta.model._meta.verbose_name

@register.filter
def form_app_url(value):
	return value._meta.model._meta.app_label.lower() + ':home'

@register.filter
def form_prefix(value):
	return slugify(value.__class__.__name__.lower())

@register.filter
def formset_model_name(value):
	return value.model._meta.verbose_name_plural.title()

"""

Model filters

"""
@register.simple_tag
def model_action(value, action):
	name =  value._meta.model._meta.app_label + ':' + value._meta.model.__name__.lower() + "_" + action
	return reverse(name, args=(value.pk,))

@register.filter
def model_name(value):
	return value._meta.verbose_name.title()

@register.filter
def model_name_plural(value):
	return value._meta.verbose_name_plural.title()

@register.filter
def model_app_name(value):
	return value._meta.verbose_name

@register.filter
def model_app_url(value):
	return value._meta.app_label.lower().replace(" ", "_") + ":home"

@register.filter
def model_url(value):
	return value._meta.model._meta.app_label + ':' + value._meta.model.__name__.lower() + '_list'

"""

Queryset filters

"""
@register.filter
def queryset_app_name(value):
	return value.model._meta.verbose_name

@register.filter
def queryset_app_url(value):
	return value.model._meta.app_label.lower() + ":home"

@register.filter
def queryset_model_name_plural(value):
	return value.model._meta.verbose_name_plural.title()

@register.filter
def queryset_model_url(value):
	return value.model.__name__.lower() + '_list'

@register.simple_tag
def queryset_action(value, action):
	name = value.model._meta.app_label + ':' +  value.model.__name__.lower() + "_" + action
	return reverse(name)