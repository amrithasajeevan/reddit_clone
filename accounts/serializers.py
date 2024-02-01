from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
# from accounts.images import serializer as images_serializers
from .models import CustomUser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        # token['age'] = user.age
        # token['gender'] = user.gender
        # token['profession'] = user.profession
        # Add more custom claims as needed

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Include additional user details in the response
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['is_superuser'] = self.user.is_superuser
        # data['age'] = self.user.age
        # data['gender'] = self.user.gender
        # data['profession'] = self.user.profession
        # Add more user details as needed

        return data

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email', 'phone', 'date_of_birth', 'password']

    def validate_username(self, value):
        # Check if the username already exists
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is already in use. Please choose another one.')
        return value

    def validate_email(self, value):
        # Check if the email is unique
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already registered. Please use a different email.')
        return value

    def validate_phone(self, value):
        # Check if the phone number is unique
        if get_user_model().objects.filter(phone=value).exists():
            raise serializers.ValidationError('This phone number is already registered. Please use a different one.')
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            date_of_birth=validated_data['date_of_birth'],
            password=validated_data['password']
        )
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    post_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_self = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model =CustomUser
        fields = (
            'profile_image',
            'username',
            'first_name',
            'bio',
            'website',
            'post_count',
            'followers_count',
            'following_count',
            'images',
            'is_self',
            'following'
        )
    
    def get_is_self(self, user):
        if 'request' in self.context:
            request =  self.context['request']
            if user.id == request.user.id:
                return True
            else:
                return False
        return False

    def get_following(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            if obj in request.user.following.all():
                return True
        return False

class ListUserSerializer(serializers.ModelSerializer):

    following = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'profile_image',
            'username',
            'first_name',
            'bio',
            'website',
            'post_count',
            'followers_count',
            'following_count',
            'following'
        )

    def get_following(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            if obj in request.user.following.all():
                return True
        return False
    
