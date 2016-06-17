# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
	url(_(r'^authors/$'), views.AuthorList.as_view(), name='author_list' ),
	url(_(r'^authors/(?P<pk>[0-9]+)/$'),views.AuthorDetail.as_view(), name='author_detail' ),
	url(_(r'^authors/(?P<pk>[0-9]+)/update/$'),views.AuthorUpdate.as_view(), name='author_update' ),
	url(_(r'^authors/(?P<pk>[0-9]+)/delete/$'),views.AuthorDelete.as_view(), name='author_delete' ),
]