from rest_framework import serializers
from base.models import Item, Item2 

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class Item2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Item2
        fields = '__all__'
