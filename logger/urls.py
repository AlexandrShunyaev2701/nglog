from rest_framework.routers import DefaultRouter
from .views import NginxLogsView
from django.urls import path, include


router = DefaultRouter()
router.register(r'nginx_log', NginxLogsView, basename='nginx_log')

urlpatterns = [
    path('', include(router.urls)),
]
