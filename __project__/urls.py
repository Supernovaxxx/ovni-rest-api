from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', admin.site.urls),
    path('', include('event.urls')),
    path('', include('rest_framework.urls')),
]