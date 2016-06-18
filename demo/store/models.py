# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Actor(models.Model):
	first_name = models.CharField(max_length=100)
	last_name  = models.CharField(max_length=100)
	image      = models.ImageField(upload_to='actor/', blank=True, null=True)

	class Meta:
		ordering            = ['last_name', 'first_name']
		verbose_name        = _('Actor')
		verbose_name_plural = _('Actors')

	def __unicode__(self):
		return '%s, %s' % (self.last_name, self.first_name)

	def get_absolute_url(self):
		return reverse_lazy('store:actor_detail', args=[self.pk, ])

	def get_actions(self):
		return (
			( _('Edit'), 'update', 'info', 'pencil' ),
			( _('Delete'), 'delete', 'danger', 'trash' ),
		)

class Contact(models.Model):
	actor   = models.OneToOneField(Actor, related_name='contact_information') # The related_name is crucial
	phone   = models.CharField(max_length=30)
	email   = models.EmailField()
	address = models.TextField(blank=True)

	def __unicode__(self):
		return '%s' % self.actor

class Movie(models.Model):
	name        = models.CharField(max_length=250)
	year        = models.PositiveIntegerField()
	description = models.TextField()
	image       = models.ImageField(upload_to='movies/',blank=True, null=True)

	class Meta:
		ordering            = ['-year', 'name']
		verbose_name        = _('Movie')
		verbose_name_plural = _('Movies')

	def __unicode__(self):
		return '%s' % self.name

	def get_absolute_url(self):
		return reverse_lazy('store:movie_detail', args=[self.pk, ])

class Cast(models.Model):
	movie       = models.ForeignKey(Movie)
	actor       = models.ForeignKey(Actor)
	name        = models.CharField(max_length=250)
	description = models.TextField(blank=True)
	image       = models.ImageField(upload_to='casts/', blank=True, null=True)

	class Meta:
		ordering            = ['name',]
		verbose_name        = _('Cast')
		verbose_name_plural = _('Casts')
	
	def __unicode__(self):
		return '%s' % self.name

	def get_absolute_url(self):
		return reverse_lazy('store:cast_detail', args=[self.pk, ])