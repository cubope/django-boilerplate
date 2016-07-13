# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import six
from django.utils.translation import ugettext_lazy as _

class NoLoginRequiredMixin(object):
	"""
	Mixin for any class view classes that required the current user
	if not authenticated, redirects the user to the home page or any
	URL with the *next* parameter.

	**Example**
	::
		class Register(NoLoginRequiredMixin, FormView):
			form_class = forms.RegisterForm
	"""
	def get(self, request, **kwargs):
		if request.user.is_authenticated():
			if request.GET.get('next', None):
				return redirect( request.GET.get('next') )
			
			return redirect('/')

		return super(NoLoginRequiredMixin, self).get(request, **kwargs)

class ListActionsMixin(object):
	"""
	Mixin for :class:`~django.views.generic.list.ListView` classes that
	adds to the "context" a variable with a list of actions.

	**Example**
	::
		class ModelList(ListActionsMixin, ListView):
			actions = (
				_('Add'), 'create', 'primary', 'plus'),
				_('Export'), 'export', 'success', 'export'),
			)
			model = Model
	"""
	def get_action_list(self):
		"""
		Return the list of actions to show in the "context".

		Override this function to personalize the list of actions.

		For example: based on the user permissions.
		"""
		return self.action_list

	def get_context_data(self, **kwargs):
		if not 'actions' in kwargs:
			kwargs['actions'] = self.get_action_list()

		return super(ListActionsMixin, self).get_context_data(**kwargs)

class CreateModelMixin(object):
	def form_valid(self, form):
		setattr(form.instance, self.field_user, self.request.user)

		return super(CreateModelMixin, self).form_valid(form)

class CRUDMessageMixin(object):
	message_action  = None
	success_message = _('%(model)s: "%(name)s" has been %(action)s successfully.')
	
	def get_success_message(self):
		"""
		Default success message mixin
		"""
		return self.success_message % dict(
			model  = self.object.__class__._meta.verbose_name.title(),
			name   = self.object,
			action = self.message_action,
		)

	def get_success_url(self):
		"""
		If the `get_sucess_url` if overwrite the message wont appear
		"""
		success_message = self.get_success_message()
		
		if success_message:
			messages.success(self.request, success_message)
		
		return super(CRUDMessageMixin, self).get_success_url()

class CreateMessageMixin(CRUDMessageMixin):
	"""
	Mixin for :class:`~django.views.generic.edit.CreateView` classes that
	adds a success message after the action is completed successfully.

	**Example**
	::
		class ModelSendEmail(CreateMessageMixin, CreateView):
			model = Model
	"""
	message_action = 'created'

class UpdateMessageMixin(CRUDMessageMixin):
	"""
	Mixin for :class:`~django.views.generic.edit.UpdateView` classes that
	adds a success message after the action is completed successfully.

	**Example**
	::
		class ModelSendEmail(UpdateMessageMixin, UpdateView):
			model = Model
	"""
	message_action = 'updated'

class DeleteMessageMixin(CRUDMessageMixin):
	"""
	Mixin for :class:`~django.views.generic.edit.DeleteView` classes that
	adds a success message after the action is completed successfully.

	**Example**
	::
		class ModelSendEmail(DeleteMessageMixin, DeleteView):
			model = Model
	"""
	message_action = 'deleted'

class ExtraFormsAndFormsetsMixin(object):
	"""
	Mixin for :class:`~django.views.generic.edit.CreateView` or
	:class:`~django.views.generic.edit.UpdateView` classes that
	adds a success message after the action is completed successfully.

	**Example**
	::
		class UserUpdate(ExtraFormsAndFormsetsMixin, UpdateView):
			model = User
			extra_form_list = (
				('profile', 'user', forms.ProfileForm),
				('credit_card', 'user', forms.ProfileForm),
			)
			formset_list = (
				(form.AddressFormSet),
				(form.PhoneFormSet),
			)
	"""
	extra_form_list = None
	formset_list    = None

	def get_extra_form_list(self):
		"""
		Returns a list of extra forms with the lookup_field,
		relation_field and form_class to use in this view.
		"""
		return self.extra_form_list

	def get_formset_list(self):
		"""
		Returns a list of formsets with the formset class to use in this view.
		"""
		return self.formset_list

	def get_extra_forms(self, form_list=None):
		"""
		Returns a list of each extra forms to be used in this view.
		"""
		output = list()
		
		if form_list is None:
			form_list = self.get_extra_form_list()

		if form_list:
			for lookup_field, relation_field, extra_form in form_list:
				output.append(
					(relation_field, extra_form(**self.get_extra_form_kwargs(lookup_field)))
				)

		return output

	def get_formsets(self, formset_list=None):
		"""
		Returns a list of formsets to be used in this view.
		"""
		output = list()
		
		if formset_list is None:
			formset_list = self.get_formset_list()

		if formset_list:
			for formset in formset_list:
				output.append(formset(**self.get_formset_kwargs()))

		return output

	def get_extra_form_kwargs(self, lookup_field):
		"""
		Returns the keyword arguments for instantiating each extra form.
		"""
		kwargs = {
			'prefix': lookup_field,
		}

		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
				'data': self.request.POST,
				'files': self.request.FILES,
			})

		if hasattr(self, 'object'):
			try:
				kwargs.update({'instance': getattr(self.object, lookup_field)})
			except:
				pass

		return kwargs


	def get_formset_kwargs(self):
		"""
		Returns the keyword arguments for instantiating each formset.
		"""
		kwargs = {}

		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
				'data': self.request.POST,
				'files': self.request.FILES,
			})

		if hasattr(self, 'object'):
			kwargs.update({'instance': self.object})

		return kwargs

	def post(self, request, *args, **kwargs):
		"""
		Handles POST requests, instantiating a form instance with the passed
		POST variables and then checked for validity.
		"""
		try:
			self.object = self.get_object()
		except:
			self.object = None

		form        = self.get_form()
		extra_forms = self.get_extra_forms()
		formsets    = self.get_formsets()

		if not form.is_valid():
			return self.form_invalid(form, extra_forms, formsets)

		for relation_field, extra_form in extra_forms:
			if not extra_form.is_valid():
				return self.form_invalid(form, extra_forms, formsets)
		
		for formset in formsets:
			if not formset.is_valid():
				return self.form_invalid(form, extra_forms, formsets)

		return self.form_valid(form, extra_forms, formsets)

	def form_valid(self, form, extra_forms, formsets):
		"""
		If the form is valid, redirect to the supplied URL.
		"""
		self.object = form.save()

		for relation_field, extra_form in extra_forms:
			setattr(extra_form.instance, relation_field, self.object)
			extra_form.save()

		for formset in formsets:
			formset.instance = self.object
			formset.save()
		
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, extra_forms, formsets):
		"""
		If the form or the extra forms are invalid, re-render the context data with the
		data-filled form and errors.
		"""
		return self.render_to_response(self.get_context_data(form=form, extra_forms=extra_forms, formsets=formsets))

	def get_context_data(self, **kwargs):
		"""
		Insert the extra forms and formsets into the context dict.
		"""
		if 'extra_forms' not in kwargs:
			kwargs['extra_forms'] = list()
			
			for relation_field, extra_form in self.get_extra_forms():
				kwargs['extra_forms'].append(extra_form)
		else:
			extra_forms = list()
			
			for relation_field, extra_form in kwargs['extra_forms']:
				extra_forms.append(extra_form)
			
			kwargs['extra_forms'] = extra_forms

		if 'formsets' not in kwargs:
			kwargs['formsets'] = self.get_formsets()
		
		return super(ExtraFormsAndFormsetsMixin, self).get_context_data(**kwargs)