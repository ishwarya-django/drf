
from rest_framework import serializers
from .models import Transformer,Product,Singer,Song
# from.serializers import SongSerializer
# from . import serializers
  
class TransformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transformer
        fields = "__all__"

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields =  ['id','product','cost','url']

        
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id','duration','title','singer']

class SingerSerializer(serializers.ModelSerializer):
    sung_by=SongSerializer(many=True,read_only=True)
    class Meta:
        model = Singer
        fields =['id','name','gender','sung_by']
