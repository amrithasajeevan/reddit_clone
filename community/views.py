from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class CommunityView(APIView):
    def get(self,request):
        com=Community.objects.all()
        ser=CommunitySerializer(com,many=True)
        return Response(data=ser.data)
    def post(self,request):
        user=request.user
        ser=CommunitySerializer(data=request.data)
        if ser.is_valid():
            ser.save(user=user)
            response_data = {
            'message': 'Community Created successfully',
            'user': ser.data
            }
            return Response(response_data,status=status.HTTP_201_CREATED)
        else:
            return Response({"Msg":ser.errors},status=status.HTTP_400_BAD_REQUEST)
        