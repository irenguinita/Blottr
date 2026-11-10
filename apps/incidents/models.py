from django.contrib.auth.models import User
from django.db import models


class IncidentCategory(models.Model):
    category_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Incident categories"

    def __str__(self):
        return self.category_name


class IncidentReport(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("under_investigation", "Under Investigation"),
        ("resolved", "Resolved"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(IncidentCategory, on_delete=models.PROTECT)
    occurrence_timestamp = models.DateTimeField()
    narrative_description = models.TextField()
    involved_parties = models.TextField(blank=True)
    latitude = models.FloatField()    # map pin (stands in for location_point)
    longitude = models.FloatField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurrence_timestamp"]

    def __str__(self):
        return f"{self.category} - {self.occurrence_timestamp:%Y-%m-%d %H:%M}"