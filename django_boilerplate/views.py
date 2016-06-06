from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import six
from django.utils.translation import ugettext_lazy as _

class NoLoginRequiredMixin(object):
	def get(self, request, **kwargs):
		if request.user.is_authenticated():
			if request.GET.get('next', None):
				return redirect( request.GET.get('next') )
			
			return redirect('/')

		return super(NoLoginRequiredMixin, self).get(request, **kwargs)

class ListActionsMixin(object):
	def get_action_list(self):
		return self.action_list

	def get_context_data(self, **kwargs):
		if not 'actions' in kwargs:
			kwargs['actions'] = self.get_action_list()

"""

User Form

"""
class CreateModelMixin(object):
	def form_valid(self, form):
		setattr(form.instance, self.field_user, self.request.user)

		return super(CreateUserMixin, self).form_valid(form)

"""

Messages

"""
class CRUDMessageMixin(six.with_metaclass(SuccessMessageMixin)):
	message_action  = None
	success_message = _('%(model)s: "%(name)s" has been %(action)s successfully.')
	
	def get_success_message(self, cleaned_data):
		"""
		Default success message mixin
		"""
		return self.success_message % dict(
			model  = self.object.__class__._meta.verbose_name.title(),
			name   = self.object,
			action = self.message_action,
		)

class CreateMessageMixin(six.with_metaclass(CRUDMessageMixin)):
	message_action = 'created'

class UpdateMessageMixin(six.with_metaclass(CRUDMessageMixin)):
	message_action = 'updated'

class DeleteMessageMixin(six.with_metaclass(CRUDMessageMixin)):
	message_action = 'deleted'

"""

Form with Extra Forms

"""
class ExtraFormsAndFormsetsMixin(object):
	def get_extra_forms_list(self):
		"""
		Returns a list of extra forms with the lookup_field, relation_field and form_class to use in this view.
		"""
		return self.extra_forms_list

	def get_formset_list(self):
		"""
		Returns a list of formsets with the formset class to use in this view.
		"""
		return self.formset_list

	def get_extra_forms(self, forms_list=None):
		"""
		Returns a list of each extra forms to be used in this view.
		"""
		output = list()
		
		if forms_list is None:
			forms_list = self.get_extra_forms_list()

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
			forms_list = self.get_formset_list()

		for formset in formset_list:
			output.append(form(**self.get_formset_kwargs()))

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
		Insert the extra forms into the context dict.
		"""
		extra_forms = self.get_extra_forms()
		formsets    = self.get_formsets()

		if len(extra_forms) > 0 and 'extra_forms' not in kwargs:
			kwargs['extra_forms'] = list()
			for relation_field, extra_form in extra_forms:
				kwargs['extra_forms'].append(extra_form)

		if len(formsets) > 0 and 'formsets' not in kwargs:
			kwargs['formsets'] = formsets
		
		return super(ExtraFormsAndFormsetsMixin, self).get_context_data(**kwargs)