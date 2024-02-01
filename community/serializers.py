from rest_framework import serializers
from .models import *

class CommunitySerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    
    class Meta:
        model=Community
        fields = [
            'community_name',
            'image',
            'content',
            'user',
            'followers',
            'followers_count'
        ]