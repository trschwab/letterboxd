from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item, Item2, MovieInfo
from .serializers import ItemSerializer, Item2Serializer, MovieInfoSerializer

@api_view(['GET'])
def getData(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addItem(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def getData2(request):
    items = Item2.objects.all()
    serializer = Item2Serializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addItem2(request):
    serializer = Item2Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def getMovieInfo(request):
    items = MovieInfo.objects.all()
    serializer = MovieInfoSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addMovieInfo(request):
    serializer = MovieInfoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
