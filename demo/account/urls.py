# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
	url(_(r'^password/$'), views.ChangePassword.as_view(), name='password'),
	url(_(r'^login/$'), views.Login.as_view(), name='login'),
	url(_(r'^logout/$'), views.Logout.as_view(), name='logout'),
	url(_(r'^registration/$'), views.Registration.as_view(), name='registration'),
	url(_(r'^recover/$'), views.Recover.as_view(), name='recover'),
	url(_(r'^recover/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$'), views.RecoverConfirm.as_view(), name='recover_confirm'),
]