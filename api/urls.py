from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('v1/', include(router.urls)),
]