from django.urls import include, path
from rest_framework.routers import DefaultRouter

from deposits.views import DepositViewSet

router = DefaultRouter()
router.register('', DepositViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
