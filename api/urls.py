from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from api.views import DishModelViewSet, MenuModelViewSet

router = DefaultRouter()
router.register('dishes', DishModelViewSet, basename='dishes')
router.register('menus', MenuModelViewSet, basename='menus')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token-auth/', views.obtain_auth_token)
]