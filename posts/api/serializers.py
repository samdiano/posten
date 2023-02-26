
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post

from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class PostSerializer(serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'likes', 'createdAt', 'updatedAt']
        read_only_fields = ['id', 'createdAt', 'updatedAt']
