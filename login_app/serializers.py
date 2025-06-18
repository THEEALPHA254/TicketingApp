# serializers.py
from .models import *
from .serializers import *
from rest_framework import serializers
from django.db.models import fields

# user model serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
       model = User
       fields = '__all__'

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")
        
        # Compare raw password directly
        if password != user.password:
            raise serializers.ValidationError("Invalid credentials.")

        data['user'] = user
        return data

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')

        if not username or not email or not password:
            raise serializers.ValidationError("Username, email, and password are required.")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists.")
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already in use.")

        # Store password as raw (no hashing)
        user = User.objects.create(**validated_data)
        user.save()
        
        return user
