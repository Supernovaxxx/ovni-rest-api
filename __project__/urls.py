"""__project__ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path
from .routers import router
from agency.sites import agency_admin_site
from geo.views import PlaceAutocomplete


urlpatterns = [
    re_path(
        r'^place-autocomplete/$',
        PlaceAutocomplete.as_view(create_field='place_id', validate_create=True),
        name='place-autocomplete',
    ),
    path("", lambda req: redirect("api/")),
    path("admin/", admin.site.urls),
    path("agency-admin/", agency_admin_site.urls),
    path("accounts/", include("allauth.urls")),
    path(
        "api/",
        include(
            [
                path("auth/", include("authentication.urls")),
                path("rest/", include("rest_framework.urls")),
                path("", include(router.urls)),
            ]
        ),
    ),
]

urlpatterns += staticfiles_urlpatterns()
