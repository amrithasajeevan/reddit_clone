from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from notifications import views 
# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from rest_auth.registration.views import SocialLoginView
# from .serializers import RegistrationSerializer
# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = MyTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Include serialized user data in the response
        response.data.update(serializer.validated_data)
        response.data['status'] = 1 

        return response

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = {
            'status':1,
            'message': 'User registered successfully',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class ExploreUsers(APIView):

    def get(self, request, format=None):

        last_five =CustomUser.objects.all().order_by('-date_joined')[:5]

        serializer = ListUserSerializer(
            last_five, many=True, context={"request": request})

        return Response({'status':1,'data':serializer.data}, status=status.HTTP_200_OK)


class FollowUser(APIView):

    def post(self, request, user_id, format=None):

        user = request.user

        try:
            user_to_follow = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.add(user_to_follow)
        user_to_follow.followers.add(user_to_follow)
        user_to_follow.save()
        user.save()

        views.create_notification(user, user_to_follow, 'follow')

        return Response({'status':1,'message':"following"},status=status.HTTP_200_OK)


class UnFollowUser(APIView):

    def post(self, request, user_id, format=None):

        user = request.user

        try:
            user_to_follow = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.remove(user_to_follow)

        user.save()

        return Response({'status':1,'message':"unfollowing"},status=status.HTTP_200_OK)


class UserProfile(APIView):

    def get_user(self, username):

        try:
            found_user = CustomUser.objects.get(username=username)
            return found_user
        except CustomUser.DoesNotExist:
            return None

    def get(self, request, username, format=None):

        found_user = self.get_user(username)

        if found_user is None:

            return Response({'status':0,'message':"user not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(
            found_user, context={'request': request})

        return Response({'status':1,'data':serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, username, format=None):

        user = request.user

        found_user = self.get_user(username)

        if found_user is None:

            return Response({'status':0,'message':"user not found"},status=status.HTTP_404_NOT_FOUND)

        elif found_user.username != user.username:

            return Response({'status':0,'message':"user not found"},status=status.HTTP_400_BAD_REQUEST)

        else:

            serializer = UserProfileSerializer(
                found_user, data=request.data, partial=True)

            if serializer.is_valid():

                serializer.save()

                return Response({'status':1,'data':serializer.data}, status=status.HTTP_200_OK)

            else:

                return Response({'status':0,'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserFollowers(APIView):

    def get(self, request, username, format=None):

        try:
            found_user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_followers = found_user.followers.all()

        serializer = ListUserSerializer(
            user_followers, many=True, context={"request": request})

        return Response({'status':1,'data':serializer.data}, status=status.HTTP_200_OK)


class UserFollowing(APIView):

    def get(self, request, username, format=None):

        try:
            found_user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_following = found_user.following.all()

        serializer = ListUserSerializer(
            user_following, many=True, context={"request": request})

        return Response({'status':1,'data':serializer.data}, status=status.HTTP_200_OK)


class Search(APIView):

    def get(self, request, format=None):

        username = request.query_params.get('username')

        if username is not None:

            users = CustomUser.objects.filter(username__istartswith=username)

            serializer = ListUserSerializer(
                users, many=True, context={"request": request})

            return Response({'status':1,'data':serializer.data}, status=status.HTTP_200_OK)

        else:

            return Response({'status':0,'data':serializer.data},status=status.HTTP_400_BAD_REQUEST)
