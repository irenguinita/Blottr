from django.urls import path
from . import views

app_name = "incidents"

urlpatterns = [
    path("", views.incident_list, name="list"),
    path("new/", views.incident_create, name="create"),
    path("map/", views.incident_map, name="map"),
    path("<int:pk>/evidence/", views.evidence_vault, name="evidence"),
]