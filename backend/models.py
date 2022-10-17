from django.db import models


# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    class Role(models.TextChoices):
        ADMIN = "ADMIN"
        REGULAR_USER = "REGULAR_USER"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.REGULAR_USER,
    )

    def __str__(self):
        return f"{self.name} -- {self.email}"


class Device(models.Model):
    description = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    consumption = models.IntegerField()


class UserDevice(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)


class Consumption(models.Model):
    user_device_id = models.ForeignKey(UserDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    consumption = models.IntegerField()
