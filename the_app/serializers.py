from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

# I wrote this code
class AppUserSerializer(serializers.ModelSerializer):
    # Define a writable username field in the serializer
    username = serializers.CharField(write_only=True)

    class Meta:
        model = AppUser
        fields = ['id', 'username', 'first_name', 'last_name', 'dob', 'pfp']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Check if the instance has a user associated with it
        if instance.user:
            data['username'] = instance.user.username
        
        return data

    def create(self, validated_data):
        # Extract the username from the validated data
        username = validated_data.pop('username', None)
        
        # Create a new user or get an existing user by username
        user, created = User.objects.get_or_create(username=username)
        
        # Create the AppUser instance with the associated user
        app_user = AppUser.objects.create(user=user, **validated_data)
        return app_user

class PostsSerializer(serializers.ModelSerializer):
    # Add a read-only field for username
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Posts
        fields = ['id', 'username', 'text', 'image', 'timestamp']

    def create(self, validated_data):
        # Access the user from the request's context
        user = self.context['request'].user
        
        # Add the user to the validated data before creating the post
        validated_data['user'] = user
        
        post = Posts.objects.create(**validated_data)
        return post
# end of code I wrote