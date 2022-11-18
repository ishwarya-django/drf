from django.shortcuts import render


from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response 
from.models import Transformer,Product,Singer,Song
from.serializers import TransformerSerializer,ProductSerializer,SingerSerializer,SongSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

  


@api_view(['GET','POST'])
def transformer_list(request):
    """
    List all transformers, or create a new transformer
    """
    if request.method == 'GET':
        transformer = Transformer.objects.all()
       
        serializer = TransformerSerializer(transformer, many=True)
        return Response(serializer.data)
  
    elif request.method == 'POST':
        serializer = TransformerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET','PUT','PATCH','DELETE'])
def transformer_detail(request, pk):
    try:
        transformer = Transformer.objects.get(pk=pk)
    except Transformer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
  
    if request.method == 'GET':
        serializer = TransformerSerializer(transformer)
        return Response(serializer.data)
  
    elif request.method == 'PUT':
        serializer = TransformerSerializer(transformer, data=request.data)
  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = TransformerSerializer(transformer,
                                           data=request.data,
                                           partial=True)
  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
  
    elif request.method == 'DELETE':
        transformer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#   viewsets

# class Trans_former(viewsets.ModelViewSet):
#     queryset=Transformer.objects.all()
#     serializer_class= TransformerSerializer

class product(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class= ProductSerializer



class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username':user.username,
            'firstname': user.first_name,
            'lastname': user.last_name
        })


class Singer_view(viewsets.ModelViewSet):
    queryset=Singer.objects.all()
    serializer_class= SingerSerializer

class Song_view(viewsets.ModelViewSet):
    queryset=Song.objects.all()
    serializer_class= SongSerializer