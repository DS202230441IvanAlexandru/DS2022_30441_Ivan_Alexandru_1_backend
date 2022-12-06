from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if username is None:
            raise TypeError('Users must have an username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    @property
    def is_staff(self):
        return self.is_superuser


class Device(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    consumption = models.IntegerField()


class UserDevice(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)


class Consumption(models.Model):
    user_device_id = models.ForeignKey(UserDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    consumption = models.FloatField()
