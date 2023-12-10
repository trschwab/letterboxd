from rest_framework import serializers
from base.models import Item, Item2, MovieInfo

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class Item2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Item2
        fields = '__all__'

class MovieInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieInfo
        fields = '__all__'

