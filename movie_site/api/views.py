from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import BasicAuthentication
from base.models import Item, Item2, MovieInfo
from .serializers import ItemSerializer, Item2Serializer, MovieInfoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework import status

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

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_movie_info(request):
    if request.method == 'GET':
        # Handle the GET request to retrieve movie information
        items = MovieInfo.objects.all()
        serializer = MovieInfoSerializer(items, many=True)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        # Handle the DELETE request to delete a movie
        movie_id = request.data.get('id')  # Assuming the ID is sent in the request data
        if movie_id:
            movie = MovieInfo.objects.filter(id=movie_id).first()
            if movie:
                movie.delete()
                return Response({'message': 'Movie deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Invalid request. Movie ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@login_required
def addMovieInfo(request):
    serializer = MovieInfoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
