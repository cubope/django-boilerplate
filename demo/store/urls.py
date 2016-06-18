# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
	url(_(r'^$'), views.MovieList.as_view(), name='movie_list' ),
	url(_(r'^movies/add/$'), views.MovieCreate.as_view(), name='movie_create' ),
	# Actor
	url(_(r'^actors/$'), views.ActorList.as_view(), name='actor_list' ),
	url(_(r'^actors/add/$'), views.ActorCreate.as_view(), name='actor_create' ),
	url(_(r'^actors/(?P<pk>[0-9]+)/$'),views.ActorDetail.as_view(), name='actor_detail' ),
	url(_(r'^actors/(?P<pk>[0-9]+)/update/$'),views.ActorUpdate.as_view(), name='actor_update' ),
	url(_(r'^actors/(?P<pk>[0-9]+)/delete/$'),views.ActorDelete.as_view(), name='actor_delete' ),
]