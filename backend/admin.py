from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Device, UserDevice, Consumption

admin.site.register(User)
admin.site.register(Device)
admin.site.register(UserDevice)
admin.site.register(Consumption)
