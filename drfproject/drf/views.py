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
import vonage
client = vonage.Client(key="77a4ddd4", secret="I9kjOb1EKRmLO3N4")
sms = vonage.Sms(client)
import xlwt
from django.http import HttpResponse


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


@api_view(['GET','POST'])
def add_product(request):
    if request.method == 'GET':
        transformer = Product.objects.all()
       
        serializer = ProductSerializer(transformer, many=True)
        return Response(serializer.data)
  
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET','POST'])
def xml_upload(request):
    if request.method == "GET":
        response = HttpResponse(content_type='application/ms-excel')

        #decide file name
        response['Content-Disposition'] = 'attachment; filename="All Complaints Report.xls"'

        #creating workbook
        wb = xlwt.Workbook(encoding='utf-8')

        #adding sheet
        ws = wb.add_sheet("sheet1")

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        # headers are bold
        font_style.font.bold = True
        #column header names, you can use your own headers here
        columns = ['Id','Name','Gender']

        #write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        
        data = Singer.objects.filter().order_by('-id')
        print(data)
        
        # data1 = Leads.objects.filter(lead_source='Youtube').order_by('-date')
        default_updated_staff = 'None'
        for my_row in data:
            row_num = row_num + 1
            ws.write(row_num, 0, row_num, font_style)
            ws.write(row_num, 1, my_row.name, font_style)
            ws.write(row_num, 2, my_row.gender, font_style)
        print(ws)
        wb.save(response) 
        print(wb)
        print(response)
        return response
    

from .task import test_func
from .task import send_mail_func
import json

# @api_view(['GET','POST'])
def test(request):
    # if request.method == "GET":

        test_func.delay()

        return HttpResponse("Done")


def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("Sent")

from django_celery_beat.models import PeriodicTask, CrontabSchedule

def schedule_mail(request):
    schedule, created= CrontabSchedule.objects.get_or_create(hour=16, minute=48)
    print("new_updateeeeeee")
    task= PeriodicTask.objects.create(crontab=schedule,name="schedule_mail_task_"+"1",task='drf.task.send_mail_func',args=json.dumps(([2,3])))
    return HttpResponse("Done")
     