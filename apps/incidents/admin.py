from django.contrib import admin
from .models import IncidentCategory, IncidentReport

admin.site.register(IncidentCategory)
admin.site.register(IncidentReport)