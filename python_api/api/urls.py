from django.contrib import admin
from django.urls import path,include
from api.views import ClientViewSet,ProjectViewSet,ProjectListCreateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'client',ClientViewSet)
router.register(r'projects', ProjectViewSet,basename='projects')
router.register(r'clients/(?P<client_id>[^/.]+)/projects', ProjectViewSet, basename='client-projects')


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
    path('api/v1/project/', ProjectListCreateView.as_view(), name='project-list-create'),

]