from rest_framework import serializers
from ddapp.models import CustomUser as User
from .models import Roadmap, Task

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class RoadmapSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Roadmap
        fields = ['title', 'description', 'owner']


class TaskSerializer(serializers.ModelSerializer):
    roadmap = RoadmapSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['title', 'description', 'roadmap']

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
