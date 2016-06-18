# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from .models import Actor, Cast, Contact, Movie

class ActorForm(forms.ModelForm):
	class Meta:
		fields = '__all__'
		model  = Actor

class ContactForm(forms.ModelForm):
	class Meta:
		exclude = ('actor', )
		model = Contact

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
MovieCastFormSet = inlineformset_factory(
	Movie,
	Cast,
	form       = CastForm,
	extra      = 3,
	can_delete = True
)