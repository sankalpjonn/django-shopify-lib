# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Shop
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import login
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.shortcuts import render
from .serializers import RedactShopSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .exceptions import *

import random, hmac, hashlib, json, base64, urllib, requests, os

class InstallView(APIView):

	def initial(self, request, *args, **kwargs):
		super(InstallView, self).initial(request, *args, **kwargs)
		request.state = str(random.randint(0, 100000000))

		if request.GET.get('shop') is None:
			raise ShopIdMissingException()


	def finalize_response(self, request, response, *args, **kwargs):
		res = super(InstallView, self).finalize_response(request, response, *args, **kwargs)
		res.set_cookie(
			'state',
			request.state,
			max_age=3600 * 24,
			expires=datetime.strftime(datetime.utcnow() + timedelta(seconds=3600 * 24), "%a, %d-%b-%Y %H:%M:%S GMT")
		)
		return res

	def get(self, request):
		return Response()

class InstallCallbackView(APIView):
	def is_hmac_verification_successful(self, params):
		cleaned_params = []
		hmac_value = params['hmac']

		# Sort parameters
		for k in sorted(params):
		    if k in ['hmac', 'signature']:
		        continue

		    cleaned_params.append((k, params[k]))

		new_qs = "&".join(["{}={}".format(i[0], i[1]) for i in cleaned_params])
		secret = settings.SHOPIFY_CLIENT_SECRET.encode("utf8")
		h = hmac.new(secret, msg=new_qs.encode("utf8"), digestmod=hashlib.sha256)

		# Compare digests
		return h.hexdigest() == hmac_value

	def initial(self, request, *args, **kwargs):
		super(InstallCallbackView, self).initial(request, *args, **kwargs)

		# verify state cookie
		if request.COOKIES.get('state') != request.GET.get('state'):
			raise OriginNotVerifiedException()

		# verify hmac signature
		if not self.is_hmac_verification_successful(request.GET):
			return SignatureMisMatchException()

		# get permanent auth token
		url = "https://{}/admin/oauth/access_token?client_id={}&client_secret={}&code={}"
		r = requests.post(
			url.format(request.GET['shop'],
				settings.SHOPIFY_CLIENT_ID,
				settings.SHOPIFY_CLIENT_SECRET,
				request.GET['code']
			),
			data=json.dumps({
				"client_id": settings.SHOPIFY_CLIENT_ID,
				"client_secret": settings.SHOPIFY_CLIENT_SECRET,
				"code": request.GET['code']
			})
		)

		if r.status_code != 200:
			return CouldNotFetchAuthTokenException()

		# create shop user if not already created
		u, _ = User.objects.get_or_create(
					username=request.GET['shop'],
					defaults = {
						"password": json.loads(r.text)['access_token']
					}
				)
		# create shop if not already created
		request.shop, _ = Shop.objects.update_or_create(
			id=request.GET['shop'],
			defaults={
				'user': u,
				'scopes': settings.SHOPIFY_SCOPES,
				'auth_token': json.loads(r.text)['access_token']
			}
		)


	def get(self, request):
		return Response()


class RedactCustomerInfoView(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(RedactCustomerInfoView, self).dispatch(*args, **kwargs)

	def post(self, request):
		return HttpResponse(status=200)

	def get(self, request):
		return HttpResponse(status=200)

class CustomerDataView(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
	    return super(CustomerDataView, self).dispatch(*args, **kwargs)

	def post(self, request):
		return HttpResponse(status=200)

	def get(self, request):
		return HttpResponse(status=200)

class RedactShopInfoView(CreateAPIView):
	serializer_class = RedactShopSerializer

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
	    return super(RedactShopInfoView, self).dispatch(*args, **kwargs)

	def post(self, request):
		meta = {key: request.META[key] for key in request.META if key.startswith("HTTP_")}
		print "REDACT: \n DATA: {} \n META: {} \n QUERY: {}".format(request.data, meta, request.GET)
		return super(RedactShopInfoView, self).post(request)
