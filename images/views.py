from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from accounts.models import *
from accounts.serializers import *
from .serializers import *
from notifications import views as notification_views
from django.shortcuts import get_object_or_404

class Images(APIView):

    def get(self, request, format=None):

        user = request.user

        following_users = user.following.all()

        image_list = []

        for following_user in following_users:

            user_images = following_user.images.all()[:2]

            for image in user_images:

                image_list.append(image)

        my_images = user.images.all()[:2]

        for image in my_images:

            image_list.append(image)

        sorted_list = sorted(
            image_list, key=lambda image: image.created_at, reverse=True)

        serializer = ImageSerializer(
            sorted_list, many=True, context={'request': request})

        return Response({'status':1,'data':serializer.data})

    def post(self, request, format=None):

        user = request.user

        serializer = InputImageSerializer(data=request.data)


        if serializer.is_valid():

            serializer.save(creator=user)

            return Response({'status':1,'data':serializer.data}, status=status.HTTP_201_CREATED)

        else:
            print(serializer.errors)
            return Response({'status':0,'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LikeImage(APIView):

    def get(self, request, image_id, format=None):

        likes = Like.objects.filter(image__id=image_id)

        like_creators_ids = likes.values('creator_id')

        users = CustomUser.objects.filter(id__in=like_creators_ids)

        serializer = ListUserSerializer(
            users, many=True, context={'request': request})

        return Response({'status':1,'data':serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, image_id, format=None):

        user = request.user

        try:
            found_image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response({'status':0,'error':'image does not exist'},status=status.HTTP_404_NOT_FOUND)

        try:
            preexisiting_like = Like.objects.get(
                creator=user,
                image=found_image
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except Like.DoesNotExist:

            new_like = Like.objects.create(
                creator=user,
                image=found_image
            )

            new_like.save()

            notification_views.create_notification(
                user, found_image.creator, 'like', found_image)

            return Response({'status':1,'message':"like"},status=status.HTTP_201_CREATED)


class UnLikeImage(APIView):

    def delete(self, request, image_id, format=None):

        user = request.user

        try:
            preexisiting_like = Like.objects.get(
                creator=user,
                image__id=image_id
            )
            preexisiting_like.delete()

            return Response({'status':1,'data':{}},status=status.HTTP_204_NO_CONTENT)

        except Like.DoesNotExist:

            return Response({'status':0,'error':'like does not exists'},status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):

        user = request.user

        try:
            found_image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(creator=user, image=found_image)

            notification_views.create_notification(
                user, found_image.creator, 'comment', found_image, serializer.data['message'])

            return Response({'status':1,'data':serializer.data}, status=status.HTTP_201_CREATED)

        else:

            return Response({'status':0,'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Comments(APIView):
    def delete(self, request, comment_id, format=None):
        user = request.user
        print(f"Deleting comment with id={comment_id} for user={user}")
        try:
            comment=get_object_or_404(Comment, id=comment_id, creator=user)
            print(comment)
            comment.delete()
            return Response({'status':1,'error':'deleted'},status=status.HTTP_204_NO_CONTENT)
        except :
            return Response({'status':0,'error':'item not found'},status=status.HTTP_404_NOT_FOUND)


class Search(APIView):

    def get(self, request, format=None):

        hashtags = request.query_params.get('hashtags', None)

        if hashtags is not None:

            hashtags = hashtags.split(",")

            images = models.Image.objects.filter(
                tags__name__in=hashtags).distinct()

            serializer = serializers.ImageSerializer(
                images, many=True, context={'request': request})

            return Response({'status':1,'data':serializer.data}, status=status.HTTP_200_OK)

        else:

            images = models.Image.objects.all()[:20]
            serializer = serializers.ImageSerializer(
                images, many=True, context={'request': request})
            return Response({'status':1,'data':serializer.data}, status=status.HTTP_200_OK)


class ModerateComments(APIView): # for the image uploaded owner

    def delete(self, request, image_id, comment_id, format=None):

        user = request.user

        try:
            comment_to_delete = Comment.objects.get(
                id=comment_id, image__id=image_id, image__creator=user)
            comment_to_delete.delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageDetail(APIView):

    def find_own_image(self, image_id, user):
        try:
            image = Image.objects.get(id=image_id, creator=user)
            return image
        except Image.DoesNotExist:
            return None

    def get(self, request, image_id, format=None):

        user = request.user

        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ImageSerializer(
            image, context={'request': request})

        return Response({'status':1,'data':serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, image_id, format=None):

        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None:

            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.InputImageSerializer(
            image, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save(creator=user)

            return Response({'status':1,'data':serializer.data}, status=status.HTTP_204_NO_CONTENT)

        else:

            return Response({'status':0,'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, image_id, format=None):

        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None:

            return Response({'status':0,'error':"image not found"},status=status.HTTP_400_BAD_REQUEST)

        image.delete()

        return Response({'status':1,'item':"deleted"},status=status.HTTP_204_NO_CONTENT)
