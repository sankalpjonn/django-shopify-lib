from rest_framework import serializers
from .models import ShopRedactRequest

class RedactShopSerializer(serializers.ModelSerializer):

    class Meta:
        model  = ShopRedactRequest
        fields = "__all__"
