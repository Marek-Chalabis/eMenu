from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from api.views import DishModelViewSet, MenuModelViewSet
from django.conf.urls import url

router = DefaultRouter()
router.register('dishes', DishModelViewSet, basename='dishes')
router.register('menus', MenuModelViewSet, basename='menus')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token-auth/', views.obtain_auth_token),
    url('v1/documentation/', get_swagger_view(title='Pastebin API')),
]
