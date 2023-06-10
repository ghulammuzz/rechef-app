from rest_framework import serializers 
from .models import User
from .tokens import create_token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

# Register User

class RegisterUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(min_length=8, write_only=True)
    password_2 = serializers.CharField(min_length=8, write_only=True)
    
    def validate(self, data):
        if data['password'] != data['password_2']:
            raise serializers.ValidationError({"message" : "Password must match"})
        if data['email'] == "":
            raise serializers.ValidationError({"message" : "Email must not empty"})
        return data    
    
    def create(self, validated_data):
        data_user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
        )
        return data_user
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', "password", "password_2"]