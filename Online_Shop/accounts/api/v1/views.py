from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserLoginSerializer
from accounts.models import User


class UserRegister(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            vd = ser_data.validated_data
            User.objects.create_user(
                phone_number=vd['phone_number'],
                email=vd['email'],
                password=vd['password']
            )
            return Response(data=ser_data.data)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        ser_data = UserLoginSerializer(data=request.POST)
        if ser_data.is_valid():
            vd = ser_data.validated_data
            user = get_object_or_404(User, phone_number=vd['phone_number'])
            login(request, user)
            return Response(ser_data.data)
        return Response(data=ser_data.errors, status=status.HTTP_401_UNAUTHORIZED)
