# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .boilerplate import messages

class ChangePasswordForm(forms.ModelForm):
	password         = forms.CharField(label=_('Current Password'), max_length=30, widget=forms.PasswordInput())
	password_new     = forms.CharField(label=_('New password'), max_length=30, widget=forms.PasswordInput())
	password_confirm = forms.CharField(label=_('Confirm new password'), max_length=30, widget=forms.PasswordInput())
	
	class Meta:
		fields = ('password', 'password_new', 'password_confirm')
		model  = User

	def clean(self):
		cleaned_data     = super(ChangePasswordForm, self).clean()
		password         = cleaned_data['password']
		password_new     = cleaned_data['password_new']
		password_confirm = cleaned_data['password_confirm']

		if password_new != password_confirm:
			self.add_error('password_new', messages().get('change_password_new') )
			self.add_error('password_confirm', messages().get('change_password_new'))
		
		elif password == password_new:
			self.add_error('password', '')
			self.add_error('password_new', '')
			self.add_error('password_confirm', '')

			raise ValidationError( messages().get('change_password_current') )

		password_error = validate_password(password_new)

		if password_error is not None:
			return password_error

	def save(self, commit=True):
		user     = super(ChangePasswordForm, self).save(commit=False)
		password = self.cleaned_data['password_new']
		
		if commit:
			user.set_password(password)
			user.save()

		return user

class LoginForm(forms.Form):
	username = forms.CharField( label=_('Username') )
	password = forms.CharField( label=_('Password'), widget=forms.PasswordInput() )

	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		username     = cleaned_data['username']
		password     = cleaned_data['password']
		user         = authenticate(username=username, password=password)

		if user is None:
			self.add_error('username', '')
			self.add_error('password', '')
			
			raise ValidationError( messages().get('login_credentials') )
		elif not user.is_active:
			self.add_error('username', '')
			self.add_error('password', '')
			
			raise ValidationError( messages().get('login_inactive') )

class RecoverAccountForm(forms.Form):
	username = forms.CharField( label='Username or Email', max_length=150 )

	def clean_username(self):
		data = self.cleaned_data['username']

		if not User.objects.filter( Q(username=data) | Q(email=data) ).exists():
			raise ValidationError( messages().get('recover_unknown') )

		return data

class RecoverAccountConfirmForm(forms.Form):
	password_new     = forms.CharField(label=_('New password'), max_length=30, widget=forms.PasswordInput())
	password_confirm = forms.CharField(label=_('Confirm new password'), max_length=30, widget=forms.PasswordInput())

	def clean(self):
		cleaned_data     = super(RecoverAccountConfirmForm, self).clean()
		password_new     = cleaned_data['password_new']
		password_confirm = cleaned_data['password_confirm']

		if password_new != password_confirm:
			self.add_error('password_new', messages().get('change_password_new'))
			self.add_error('password_confirm', messages().get('change_password_new'))

		password_error = validate_password(password_new)

		if password_error is not None:
			return password_error

class RegistrationForm(forms.ModelForm):
	username   = forms.CharField( label=_('Username') )
	email      = forms.EmailField( label=_('Email') )
	email2     = forms.EmailField( label=_('Confirm Email') )
	password   = forms.CharField( label=_('Password'), widget=forms.PasswordInput() )
	password2  = forms.CharField( label=_('Confirm Password'), widget=forms.PasswordInput() )
	first_name = forms.CharField( label=_('Name') )
	last_name  = forms.CharField( label=_('Last Name') )

	class Meta:
		model  = User
		fields = ['username', 'email', 'email2', 'password', 'password2', 'first_name', 'last_name']

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		email     = cleaned_data.get('email')
		email2    = cleaned_data.get('email2')
		password  = cleaned_data.get('password')
		password2 = cleaned_data.get('password2')

		if password != password2:
			self.add_error('password',  messages().get('registration_password'))
			self.add_error('password2', messages().get('registration_password'))

		if email != email2:
			self.add_error('email', messages().get('registration_email'))
			self.add_error('email2', messages().get('registration_email'))

	def clean_username(self):
		data = self.cleaned_data['username']

		if User.objects.filter(username=data).exists():
			raise forms.ValidationError(messages().get('registration_username_already'))

		return data

	def clean_email(self):
		data = self.cleaned_data['email']

		if User.objects.filter(email=data).exists():
			raise forms.ValidationError(messages().get('registration_email_already'))

		return data

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password'])

		if commit:
			user.save()
			
		return user