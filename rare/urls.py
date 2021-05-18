from django.contrib import admin
from django.urls import path
from rareapi.views import login_user, register_user, TagView
from rest_framework import routers
from django.conf.urls import include

router = routers.DefaultRouter(trailing_slash=False)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tags', TagView, 'tag')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls))
]
