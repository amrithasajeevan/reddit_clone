from rest_framework import serializers
from .models import *
from accounts.serializers import RegistrationSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class CommunitySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ['id', 'community_name', 'image', 'content', 'user', 'followers', 'user_name']
        extra_kwargs = {
            'followers': {'required': False}
            
        }

    def get_followers(self, obj):
        followers_data = []
        for follower in obj.followers.all():
            follower_data = {
                'user_id': follower.id,
                'username': follower.username
            }
            followers_data.append(follower_data)
        return followers_data

    def create(self, validated_data):
        followers_data = validated_data.pop('followers', [])
        community = Community.objects.create(**validated_data)
        community.followers.set(followers_data)
        return community

from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CommunityPostSerializer(serializers.ModelSerializer):
    community_name = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    extra_kwargs = {
            'liked_by': {'required': False}
            
        }

    class Meta:
        model = CommunityPost
        fields = ['id', 'community_name', 'author_name', 'image', 'caption', 'created_at','liked_by','total_likes']

    def get_community_name(self, obj):
        return obj.community.community_name

    def get_author_name(self, obj):
        return obj.author.username
    
    def get_liked_by(self, obj):
        liked_users = obj.liked_by.all()
        return [user.username for user in liked_users]

    def get_total_likes(self, obj):
        return obj.liked_by.count()
    
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = []


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True) # Translate user ID to username

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        extra_kwargs = {
            'post': {'required': False}
        }

    def create(self, validated_data):
        return Comment.objects.create(author=self.context['author'], **validated_data)
