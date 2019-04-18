from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from app.views import NestingView

router = routers.DefaultRouter()


api_v1 = [
    path('nest/', NestingView.as_view()),
    path('deposit/', include('deposits.urls')),
    path('', include(router.urls)),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((api_v1, 'api'), namespace='v1')),
]
