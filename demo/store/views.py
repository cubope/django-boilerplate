# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from boilerplate.views import CreateMessageMixin, DeleteMessageMixin, ExtraFormsAndFormsetsMixin, ListActionsMixin, UpdateMessageMixin

from . import forms 
from .models import Actor, Movie

class ActorList(ListActionsMixin, ListView):
	action_list = (
		( _('Add'), 'create', 'primary', 'plus'),
	)
	model       = Actor
	paginate_by = 30

class ActorDetail(DetailView):
	model = Actor

class ActorCreate(CreateMessageMixin, ExtraFormsAndFormsetsMixin, CreateView):
	extra_form_list = (
		'contact_information', 'user', forms.ContactInformationForm,
	)
	form_class      = forms.ActorForm
	model           = Actor

class MovieCreate(CreateMessageMixin, ExtraFormsAndFormsetsMixin, CreateView):
	form_class   = forms.MovieForm
	formset_list = (
		forms.MovieCastFormSet,
	)
	model        = Movie