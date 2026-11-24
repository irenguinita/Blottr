from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class IncidentCategory(models.Model):
    category_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Incident categories"

    def __str__(self):
        return self.category_name


class Barangay(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default="Cebu City")

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "city")

    def __str__(self):
        return f"{self.name}, {self.city}"


class Station(models.Model):
    name = models.CharField(max_length=150)
    barangay = models.ForeignKey(
        Barangay,
        on_delete=models.PROTECT,
        related_name="stations",
    )
    address = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class IncidentReport(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("under_investigation", "Under Investigation"),
        ("resolved", "Resolved"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(IncidentCategory, on_delete=models.PROTECT)
    barangay = models.ForeignKey(
        Barangay,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="incident_reports",
    )
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

class EvidenceFile(models.Model):
    IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")

    report = models.ForeignKey(
        IncidentReport,
        on_delete=models.CASCADE,
        related_name="evidence_files",
    )
    file = models.FileField(upload_to="evidence/%Y/%m/")
    original_name = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.original_name or self.file.name

    @property
    def is_image(self):
        return self.file.name.lower().endswith(self.IMAGE_EXTENSIONS)


class GeneratedReport(models.Model):
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="generated_reports",
    )
    barangay = models.ForeignKey(
        Barangay,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="generated_reports",
    )  # null means "all barangays"
    date_range_start = models.DateField()
    date_range_end = models.DateField()
    file_path = models.CharField(max_length=255, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self):
        return f"Report {self.date_range_start} to {self.date_range_end} ({self.generated_at:%Y-%m-%d %H:%M})"