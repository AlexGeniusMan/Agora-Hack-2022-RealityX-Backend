from rest_framework import serializers

from main_app.models import Page, Product


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 0
        model = Page
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 0
        model = Product
        fields = '__all__'
