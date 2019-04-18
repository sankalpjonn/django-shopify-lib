# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
	id               = models.CharField(max_length=250, primary_key=True)
	user             = models.ForeignKey(User)
	scopes           = models.CharField(max_length=250)
	auth_token       = models.CharField(max_length=250)
	created_at       = models.DateTimeField(auto_now_add=True)
	last_updated_on  = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.id

class ShopRedactRequest(models.Model):
    shop_id     = models.BigIntegerField(primary_key=True)
    shop_origin = models.CharField(max_length=255)

    def __unicode__(self):
        return "{}_{}".format(self.shop_id, self.shop_origin)
