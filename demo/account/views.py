from django.core.urlresolvers import reverse_lazy
from boilerplate.views import (ChangePasswordView, LoginView, LogoutView, 
	RecoverAccountView, RecoverAccountConfirmView, RegistrationView)

class ChangePassword(ChangePasswordView):
	template_name = 'account/password.html'

class Login(LoginView):
	template_name = 'account/login.html'

class Logout(LogoutView):
	success_url = reverse_lazy('store:movie_list')

class Recover(RecoverAccountView):
	recover_url   = 'account:recover_confirm'
	success_url   = reverse_lazy('store:movie_list')
	template_name = 'account/recover.html'

class RecoverConfirm(RecoverAccountConfirmView):
	success_url   = reverse_lazy('account:login')
	template_name = 'account/recover_confirm.html'

class Registration(RegistrationView):
	success_url   = reverse_lazy('store:movie_list')
	template_name = 'account/registration.html'