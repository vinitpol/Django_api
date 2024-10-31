from django.contrib import admin
from django.urls import path,include
from api.views import ClientViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'client',ClientViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('api/v1/client/<int:pk>/', ClientViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('api/v1/client/', ClientViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),

]