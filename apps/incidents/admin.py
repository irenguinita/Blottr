from django.contrib import admin
from .models import IncidentCategory, IncidentReport, Barangay, Station

admin.site.register(IncidentCategory)
admin.site.register(IncidentReport)
admin.site.register(Barangay)
admin.site.register(Station)