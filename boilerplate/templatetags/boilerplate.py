# -*- coding: utf-8 -*-
import unicodedata
from django import template
from django.contrib.admin.utils import NestedObjects
from django.core.urlresolvers import reverse
from django.db import DEFAULT_DB_ALIAS
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
	"""
	List the related objects before delete an object
	"""
	collector = NestedObjects(using=DEFAULT_DB_ALIAS)
	collector.collect([object])
	
	return collector.nested()

"""

Form filters

"""
@register.filter
def form_model_name(value):
	"""
	Return the model verbose name of a form model
	"""
	return value._meta.model._meta.verbose_name

@register.filter
def form_model_name_plural(value):
	"""
	Return the model verbose name plural of a form model
	"""
	return value._meta.model._meta.verbose_name_plural

@register.filter
def form_model_url(value):
	"""
	Return the model list url name of a form model
	"""
	return value._meta.model._meta.app_label + ':' + value._meta.model.__name__.lower() + '_list'

@register.filter
def form_app_name(value):
	"""
	Return the app name of a form model
	"""
	return value._meta.model._meta.app_config.verbose_name

@register.filter
def form_app_url(value):
	"""
	Return the app home url of a form model
	"""
	return value._meta.model._meta.app_label.lower() + ':home'

@register.filter
def form_prefix(value):
	"""
	Return the form name as a prefix
	"""
	return slugify(value.__class__.__name__.lower())

@register.filter
def formset_model_name(value):
	"""
	Return the model verbose name of a formset
	"""
	return value.model._meta.verbose_name

@register.filter
def formset_model_name_plural(value):
	"""
	Return the model verbose name plural of a formset
	"""
	return value.model._meta.verbose_name_plural

"""

Model filters

"""
@register.simple_tag
def model_action(value, action):
	"""
	**Tag name**
	::
		model_action
	
	Return the full url name of an action
	
	**Usage**
	::
		{% model_action object action %}
	
	**Example**
	::
		{% model_action object 'update' %}
	"""
	name =  value._meta.model._meta.app_label + ':' + value._meta.model.__name__.lower() + "_" + action
	return reverse(name, args=(value.pk,))

@register.filter
def model_name(value):
	"""
	Return the model verbose name of an object
	"""
	return value._meta.verbose_name

@register.filter
def model_name_plural(value):
	"""
	Return the model verbose name plural of an object
	"""
	return value._meta.verbose_name_plural

@register.filter
def model_app_name(value):
	"""
	Return the app verbose name of an object
	"""
	return value._meta.app_config.verbose_name

@register.filter
def model_app_url(value):
	"""
	Return the app home url of an object
	"""
	return value._meta.app_label.lower().replace(" ", "_") + ":home"

@register.filter
def model_url(value):
	"""
	Return the model list url name of a model
	"""
	return value._meta.model._meta.app_label + ':' + value._meta.model.__name__.lower() + '_list'

"""

Queryset filters

"""
@register.filter
def queryset_app_name(value):
	"""
	Return the app verbose name of a queryset
	"""
	return value.model._meta.app_config.verbose_name

@register.filter
def queryset_app_url(value):
	"""
	Return the app home url name of a queryset
	"""
	return value.model._meta.app_label.lower() + ":home"

@register.filter
def queryset_model_name_plural(value):
	"""
	Return the app verbose name plural of a queryset
	"""
	return value.model._meta.verbose_name_plural

@register.filter
def queryset_model_url(value):
	"""
	Return the model list url name of a queryset
	"""
	return value.model.__name__.lower() + '_list'

@register.simple_tag
def queryset_action(value, action):
	"""
	**Tag name**
	::
		queryset_action
	
	Return the full url name of an action

	**Parameters**:
			:queryset: A valid queryset of objects

			:action: A valid action name. Ex. namespace:model_action
	
	**Usage**
	::
		{% queryset_action queryset action %}
	
	**Example**
	::
		{% queryset_action queryset 'add' %}
	"""
	name = value.model._meta.app_label + ':' +  value.model.__name__.lower() + "_" + action
	return reverse(name)