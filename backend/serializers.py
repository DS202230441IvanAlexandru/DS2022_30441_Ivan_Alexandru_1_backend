from rest_framework import serializers

from .models import User, Device, UserDevice, Consumption


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'role')


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'description', 'address', 'consumption')


class UserDeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserDevice
        fields = ('id', 'user_id', 'device_id')


class ConsumptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Consumption
        fields = ('id', 'timestamp', 'consumption')
