# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms import inline_formset_factory
from django.utils.translation import ugettext_lazy as _

from .models import Actor, Cast, ContactInformation, Movie

class ActorForm(forms.ModelForm):
	class Meta:
		fields = '__all__'
		model  = Actor

class ContactInformation(forms.ModelForm):
	class Meta:
		fields = '__all__' # If you set the "actor" field "editable=False", otherwise use:
		# exclude = ('actor', )
		model = ContactInformation

class MovieForm(forms.ModelForm):
	class Meta:
		fields = '__all__'
		model  = Movie

class CastForm(forms.ModelForm):
	class Meta:
		fields = '__all__'
		model  = Cast

"""
Formsets
"""
MovieCastFormSet = inline_formset_factory(
	Movie,
	Cast,
	form       = CastForm,
	extra      = 3,
	can_delete = True
)