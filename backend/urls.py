from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .jwt.tokenPairSerializer import TokenSerializerView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'userDevices', views.UserDeviceViewSet)
router.register(r'consumptions', views.ConsumptionViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('token/', TokenSerializerView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
