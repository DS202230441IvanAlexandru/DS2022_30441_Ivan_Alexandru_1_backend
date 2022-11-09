from datetime import datetime

import jwt
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from EUP_backend import settings
from .serializers import UserSerializer, DeviceSerializer, UserDeviceSerializer, ConsumptionSerializer, LoginSerializer, \
    RetrieveUserDeviceSerializer, CreateUserSerializer
from .models import User, Device, UserDevice, Consumption
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = User.objects.all().order_by('email')

    def get_queryset(self):
        queryset = User.objects.all().order_by('email')
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(email__contains=email)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        else:
            return UserSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all().order_by('description')
    serializer_class = DeviceSerializer

    def get_queryset(self):
        queryset = Device.objects.all().order_by('name')
        userId = self.request.query_params.get("userId")
        print(userId)
        if userId:
            queryset = Device.objects.filter(userdevice__user_id=userId).order_by("name")
            return queryset
        return queryset


class UserDeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = UserDevice.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RetrieveUserDeviceSerializer
        else:
            return UserDeviceSerializer


class ConsumptionViewSet(viewsets.ModelViewSet):
    queryset = Consumption.objects.all().order_by('timestamp')
    serializer_class = ConsumptionSerializer

    def get_queryset(self):
        queryset = Consumption.objects.all().order_by('timestamp')
        userId = self.request.query_params.get("userId")
        deviceId = self.request.query_params.get("deviceId")
        dateParam = self.request.query_params.get("date")
        print(userId)
        print(deviceId)
        print(dateParam)
        if userId and deviceId and dateParam:
            date = datetime.strptime(dateParam, '%d/%m/%y')
            queryset = Consumption.objects.filter(user_device_id__device_id=deviceId, user_device_id__user_id=userId,
                                                  timestamp__day=date.day, timestamp__month=date.month)
            return queryset
        return queryset


class LoginAPIView(APIView):
    def get(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        payload = jwt.decode(access_token, key=settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload["user_id"]

        user = User.objects.get(pk=user_id)
        userDTO = UserSerializer(user)

        return Response(userDTO.data, status=status.HTTP_200_OK)
