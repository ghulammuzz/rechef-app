from rest_framework import serializers 
from .models import User, Interest
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

# Register User

class RegisterUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(min_length=8, write_only=True)
    password_2 = serializers.CharField(min_length=8, write_only=True)
    image = serializers.ImageField(required=False)
    interest = serializers.ListField(required=True)
    gender = serializers.CharField(required=True)
    
    def to_representation(self, instance):
        list_interest = []
        for i in instance.interest.all():
            list_interest.append(i.interest)
        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "gender" : instance.gender,
            "interest": list_interest,
        }
    
    def validate(self, data):
        
        interest = data.pop('interest')
        gender = data['gender']
        
        if gender != "Women" and "Men":
            print(gender)
            raise serializers.ValidationError({"message" : "Gender must match"})
            
        if interest:
            list_interest = []
            for i in interest:
                list_interest.append(get_object_or_404(Interest, interest=i))
            data['interest'] = list_interest
            
        if data['password'] != data['password_2']:
            raise serializers.ValidationError({"message" : "Password must match"})
        if data['email'] == "":
            raise serializers.ValidationError({"message" : "Email must not empty"})
        
        return data
    
    def create(self, validated_data):
        interest = validated_data.pop('interest')
        gender = validated_data.pop('gender')
        
        data_user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
            gender = gender
        )
        
        for i in interest:
            data_user.interest.add(i)
        return data_user
    
    class Meta:
        model = User
        fields = ['id', "username", "gender", 'email', "interest", "image", "password", "password_2"]