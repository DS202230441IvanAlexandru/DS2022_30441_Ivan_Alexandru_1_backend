from django.shortcuts import render

from rest_framework import viewsets

from .serializers import UserSerializer, DeviceSerializer, UserDeviceSerializer, ConsumptionSerializer
from .models import User, Device, UserDevice, Consumption


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('email')
    serializer_class = UserSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all().order_by('description')
    serializer_class = DeviceSerializer


class UserDeviceViewSet(viewsets.ModelViewSet):
    queryset = UserDevice.objects.all().order_by('id')
    serializer_class = UserDeviceSerializer


class ConsumptionViewSet(viewsets.ModelViewSet):
    queryset = Consumption.objects.all().order_by('timestamp')
    serializer_class = ConsumptionSerializer
