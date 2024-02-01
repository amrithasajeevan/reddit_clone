from rest_framework import serializers
# from taggit_serializer.serializers import (TagListSerializerField,
#                                            TaggitSerializer)
from .models import *
from accounts.models import *


class SmallImageSerializer(serializers.ModelSerializer):

    """ Used for the notifications """

    class Meta:
        model = Image
        fields = (
            'file',
        )


class CountImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = (
            'id',
            'file',
            'comment_count',
            'like_count'
        )


class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'profile_image',
            'username',
            'first_name',
            'bio',
            'website',
            'post_count',
            'followers_count',
            'following_count',
        )


class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'message',
            'creator'
        )


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'


class ImageSerializer( serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'like_count',
            'creator',
            'natural_time',
            'is_liked',
            'is_vertical'
        )

    def get_is_liked(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            try:
                Like.objects.get(
                    creator__id=request.user.id, image__id=obj.id)
                return True
            except Like.DoesNotExist:
                return False
        return False


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = (
            'creator',
        )


class InputImageSerializer(serializers.ModelSerializer):



    class Meta:
        model = Image
        fields = (
            'file',
            'location',
            'caption',

        )
