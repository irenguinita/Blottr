"""
Root URL config. Each feature app owns its own urls.py — this file just
routes prefixes to the right feature, per the vertical slicing guide.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", include("apps.login.urls")),
    path("register/", include("apps.register.urls")),
    path("", include("apps.home.urls")),   # Home is the root/landing feature
    path("profile/", include("apps.user_profile.urls")),
    path("settings/", include("apps.user_settings.urls")),
    path("incidents/", include("apps.incidents.urls")),
]
