from django.urls import path, include

urlpatterns = [
    path('', include('event.urls')),
    path('', include('rest_framework.urls')),
]