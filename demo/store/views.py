# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from boilerplate.mixins import CreateMessageMixin, DeleteMessageMixin, ExtraFormsAndFormsetsMixin, ListActionsMixin, UpdateMessageMixin

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

class ActorCreate(ExtraFormsAndFormsetsMixin, CreateMessageMixin, CreateView):
	extra_form_list = (
		('contact_information', 'actor', forms.ContactForm),
	)
	form_class      = forms.ActorForm
	model           = Actor

class ActorUpdate(ExtraFormsAndFormsetsMixin, UpdateMessageMixin, UpdateView):
	extra_form_list = (
		('contact_information', 'actor', forms.ContactForm),
	)
	form_class      = forms.ActorForm
	model           = Actor

class ActorDelete(DeleteMessageMixin, DeleteView):
	model                = Actor
	success_url          = reverse_lazy('store:actor_list')
	template_name_suffix = '_form'

class MovieList(ListActionsMixin, ListView):
	action_list = (
		( _('Add'), 'create', 'primary', 'plus'),
	)
	model       = Movie
	paginate_by = 30

class MovieCreate(ExtraFormsAndFormsetsMixin, CreateMessageMixin, CreateView):
	form_class   = forms.MovieForm
	formset_list = (
		forms.MovieCastFormSet,
	)
	model        = Movie