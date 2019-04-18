from django.conf.urls import *

from .views import *

urlpatterns = [
	## SDK APIs
	url(r'^$', InstallView.as_view(), name='install'),
	url(r'^cb$', InstallCallbackView.as_view(), name='install-cb'),
	url(r'^customer/redact$', RedactCustomerInfoView.as_view(), name='customer-redact'),
	url(r'^customer/data$', CustomerDataView.as_view(), name='customer-data'),
	url(r'^shop/redact$', RedactShopInfoView.as_view(), name='customer-data'),
]
