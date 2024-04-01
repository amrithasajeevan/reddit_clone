from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from notifications import views
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

class MyCommunity(APIView):
    def get(self,request):
        user=request.user
        com=Community.objects.filter(user=user)        
        ser=CommunitySerializer(com)
        return Response(data=ser.data)
    def put(self,request):
        user= request.user
        try:
            com=Community.objects.get(user=user)
            ser=CommunitySerializer(data=request.data,instance=com) 
            if ser.is_valid():
                ser.save()
                return Response({"msg":"Community Updated"})
            else:
                return Response({"msg":ser.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"msg":"Invalid ID"},status=status.HTTP_400_BAD_REQUEST)


class FollowCommunity(APIView):

    def post(self, request, **kwargs):

        user = request.user
        
        try:
            id=kwargs.get('pk')
            print(id)
            community_to_follow = Community.objects.get(id=id)
            print(community_to_follow)
        except Community.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.community.add(community_to_follow)
        community_to_follow.followers.add(community_to_follow)
        community_to_follow.save()
        user.save()

        views.create_notification(user, community_to_follow, 'follow')

        return Response(status=status.HTTP_200_OK)


# class UnFollowUser(APIView):

#     def post(self, request, user_id, format=None):

#         user = request.user

#         try:
#             user_to_follow = CustomUser.objects.get(id=user_id)
#         except CustomUser.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         user.following.remove(user_to_follow)

#         user.save()

#         return Response(status=status.HTTP_200_OK)