from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status


class ShopIdMissingException(APIException):
	status_code = 500
	default_detail = 'Missing shop id'

class OriginNotVerifiedException(APIException):
    status_code = 403
    default_detail = 'Origin not verified'

class SignatureMisMatchException(APIException):
    status_code = 403
    default_detail = 'Signature mismatch'

class CouldNotFetchAuthTokenException(APIException):
    status_code = 500
    default_detail = 'Could not fetch auth token'
