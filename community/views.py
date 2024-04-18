from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from notifications import views
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.


# class CommunityView(APIView):
#     def get(self,request):
#         com=Community.objects.all()
#         ser=CommunitySerializer(com,many=True)
#         return Response(data=ser.data)
#     def post(self,request):
#         user=request.user
#         ser=CommunitySerializer(data=request.data)
#         if ser.is_valid():
#             ser.save(user=user)
#             response_data = {
#             'message': 'Community Created successfully',
#             'user': ser.data
#             }
#             return Response(response_data,status=status.HTTP_201_CREATED)
#         else:
#             return Response({"Msg":ser.errors},status=status.HTTP_400_BAD_REQUEST)

# class MyCommunity(APIView):
#     def get(self,request):
#         user=request.user
#         com=Community.objects.filter(user=user)        
#         ser=CommunitySerializer(com)
#         return Response(data=ser.data)
#     def put(self,request):
#         user= request.user
#         try:
#             com=Community.objects.get(user=user)
#             ser=CommunitySerializer(data=request.data,instance=com) 
#             if ser.is_valid():
#                 ser.save()
#                 return Response({"msg":"Community Updated"})
#             else:
#                 return Response({"msg":ser.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
#         except:
#             return Response({"msg":"Invalid ID"},status=status.HTTP_400_BAD_REQUEST)


# class FollowCommunity(APIView):

#     def post(self, request, **kwargs):

#         user = request.user
        
#         try:
#             id=kwargs.get('pk')
#             print(id)
#             community_to_follow = Community.objects.get(id=id)
#             print(community_to_follow)
#         except Community.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         user.community.add(community_to_follow)
#         community_to_follow.followers.add(community_to_follow)
#         community_to_follow.save()
#         user.save()

#         views.create_notification(user, community_to_follow, 'follow')

#         return Response(status=status.HTTP_200_OK)


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

class CommunityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response({'status':1,"data":serializer.data})

    def post(self, request):
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status':1,"data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status':0,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class CommunityDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, community_id):
        community = get_object_or_404(Community, pk=community_id)
        serializer = CommunitySerializer(community)
        return Response(serializer.data)

    def patch(self, request, community_id):
        community = get_object_or_404(Community, pk=community_id)
        serializer = CommunitySerializer(community, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, community_id):
        community = get_object_or_404(Community, pk=community_id)
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CommunityListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response({'status':1,"data":serializer.data})
    


from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowCommunityAPIView(APIView):
    def post(self, request, community_id):
        community = get_object_or_404(Community, pk=community_id)
        
        # Add the current user to the followers of the community
        request.user.communities_following.add(community)
        
        return Response({'status':1,"data":{},"message": "You are now following the community"}, status=status.HTTP_200_OK)
    

from rest_framework import status

class CommunityPostAPIView(APIView):
    def post(self, request, format=None):
        serializer = CommunityPostSerializer(data=request.data)
        if serializer.is_valid():
            community_name = request.data.get('community_name')  # Extract community_name from request data
            try:
                community = Community.objects.get(community_name=community_name)
            except Community.DoesNotExist:
                return Response({"error": f"Community with name '{community_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            # Set the author as the logged-in user
            author = request.user

            # Save the post
            serializer.save(community=community, author=author)
            
            return Response({'status':1,'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status':0,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        posts = CommunityPost.objects.all()
        serializer = CommunityPostSerializer(posts, many=True)
        return Response({'status':1,"data":serializer.data})
    


class LikePostAPIView(APIView):
    def post(self, request, post_id, *args, **kwargs):
        try:
            post = CommunityPost.objects.get(pk=post_id)
        except CommunityPost.DoesNotExist:
            return Response("Post does not exist.", status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        post.liked_by.add(user)
        liked_users = post.liked_by.all()
        liked_user_names = [liked_user.username for liked_user in liked_users]
        return Response({'status':1,"message":"Post liked successfully.","data": liked_user_names}, status=status.HTTP_200_OK)
    



class CommentCreateView(APIView):
    def get(self, request, post_id):
        comments = Comment.objects.filter(post=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response({'status':1,'data':serializer.data})
    
    def post(self, request, post_id):
        post = get_object_or_404(CommunityPost, id=post_id)
        
        # Resolve author by username
        author_username = request.data.get('author', None)
        if author_username:
            author = CustomUser.objects.filter(username=author_username).first()
            if not author:
                return Response({'status':0,'error':serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status':0,'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        # Prepare comment data
        comment_data = {
            'post': post.id,
            'content': request.data.get('content')  # Extract content from request data
        }

        serializer = CommentSerializer(data=comment_data, context={'author': author})  # Pass author to serializer context
        if serializer.is_valid():
            serializer.save()  # No need to pass author here as it's in the context
            return Response({'status':1,'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status':0,'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


class CommentDetailView(APIView):
    def get(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, post=post_id)
        serializer = CommentSerializer(comment)
        return Response({'status':1,'data':serializer.data})

    def put(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, post=post_id)

        # Check if the user is the author of the comment
        if comment.author != request.user:
            return Response({'status':0,'data':serializer.errors}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':1,'data':serializer.data})
        return Response({'status':0,'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, post=post_id)

        # Check if the user is the author of the comment
        if comment.author != request.user:
            return Response({'status':0,"error": "You don't have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({'status':1,'message':"data deleted"},status=status.HTTP_204_NO_CONTENT)
