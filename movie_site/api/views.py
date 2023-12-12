from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import BasicAuthentication
from base.models import Item, Item2, MovieInfo
from .serializers import ItemSerializer, Item2Serializer, MovieInfoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

@api_view(['GET'])
@login_required
def getData(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@login_required
def addItem(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        print("valid data for serializer")
        serializer.save()
    else:
        print("invalid data for serializer")
    return Response(serializer.data)

@api_view(['GET'])
@login_required
def getData2(request):
    items = Item2.objects.all()
    serializer = Item2Serializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@login_required
def addItem2(request):
    serializer = Item2Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@login_required
def getMovieInfo(request):
    items = MovieInfo.objects.all()
    serializer = MovieInfoSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@login_required
def addMovieInfo(request):
    serializer = MovieInfoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
