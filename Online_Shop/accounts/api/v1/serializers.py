from django.contrib.auth import authenticate
from rest_framework import serializers
from accounts.models import User
from orders.models import OrderItem


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # validate method override
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('passwords dont match')
        return data


class UserLoginSerializer(serializers.Serializer):
    phone_number=serializers.CharField(max_length=11,min_length=11)
    password=serializers.CharField(write_only=True)






