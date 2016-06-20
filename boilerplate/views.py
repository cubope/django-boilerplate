# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.views.generic.edit import CreateView, FormView, UpdateView

from . import forms
from boilerplate import messages as boilerplate_messages, recover_url_name, site_name
from mail import send_html_mail
from mixins import NoLoginRequiredMixin

class ChangePasswordView(LoginRequiredMixin, UpdateView):
	form_class    = forms.ChangePasswordForm
	model         = User
	success_url   = '/'

	def get_object(self):
		return self.request.user

	def form_valid(self, form):
		user = authenticate(username=self.request.user.username, password=form.cleaned_data['password'])

		if user is None:
			form.add_error('username', '')
			form.add_error('password', '')

			raise ValidationError(_('Password is incorrect. Please verify your password.'))

		return super(ChangePasswordView, self).form_valid(form)

class LoginView(NoLoginRequiredMixin, FormView):
	form_class = forms.LoginForm

	def form_valid(self, form):
		response = super(LoginView, self).form_valid(form)

		username = form.cleaned_data['username']
		password = form.cleaned_data['password']

		user = authenticate(username=username, password=password)

		if user is not None and user.is_active:
			login(self.request, user)

		return response

	def get_success_url(self):
		if self.request.GET.get('next', None):
			return self.request.GET.get('next')
		else:
			return '/'

class LogoutView(LoginRequiredMixin, View):
	def get(self, request, **kwargs):
		logout(request)

		if request.GET.get('next', None):
			return redirect(request.GET.get('next'))
		else:
			return redirect('/')

class RecoverAccountView(NoLoginRequiredMixin, FormView):
	form_class  = forms.RecoverAccountForm
	success_url = '/'
	recover_url = None
 
	def form_valid(self, form):
		username = form.cleaned_data['username']
		user     = User.objects.get( Q(username=username) | Q(email=username) )
		object   = {
			'email': user.email,
			'domain': self.request.META['HTTP_HOST'],
			'site_name': site_name(),
			'url_name': self.recover_url,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			'user': user,
			'token': default_token_generator.make_token(user),
			'protocol': 'http',
		}
		messages.success(self.request, boilerplate_messages().get('recover_sent') % dict(email=user.email))

		send_html_mail(user, 'recover-account', boilerplate_messages().get('recover_subject') % dict(site_name=site_name()), object, site_name())
		
		return super(RecoverAccountView, self).form_valid(form)

class RecoverAccountConfirmView(NoLoginRequiredMixin, FormView):
	form_class    = forms.RecoverAccountConfirmForm
	success_url   = '/'

	def post(self, request, uidb64=None, token=None, *arg, **kwargs):
		form = self.get_form()
		assert uidb64 is not None and token is not None  # checked by URLconf
		
		try:
			uid  = urlsafe_base64_decode(uidb64)
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None

		if user is not None and default_token_generator.check_token(user, token):
			if form.is_valid():
				user.set_password(form.cleaned_data['password_new'])
				user.save()
				messages.success(request, _('Password has been reset successfully.'))
				return self.form_valid(form)
			else:
				messages.error(request, _('Password reset has been unsuccessful.'))
				return self.form_invalid(form)
		else:
			messages.error(request, _('The reset password link is no longer valid. Request a new one.'))
			return self.form_invalid(form)

class RegistrationView(NoLoginRequiredMixin, CreateView):
	form_class    = forms.RegistrationForm
	model         = User
	success_url   = '/'