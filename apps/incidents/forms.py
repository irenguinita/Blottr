from django import forms
from .models import IncidentReport


class IncidentReportForm(forms.ModelForm):
    occurrence_timestamp = forms.DateTimeField(
        label="Date and time of incident",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = IncidentReport
        fields = [
            "category",
            "occurrence_timestamp",
            "narrative_description",
            "involved_parties",
            "latitude",
            "longitude",
        ]
        labels = {
            "narrative_description": "Narrative description",
            "involved_parties": "Involved parties",
        }
        widgets = {
            "narrative_description": forms.Textarea(attrs={"rows": 5}),
            "involved_parties": forms.Textarea(attrs={"rows": 3}),
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
        }
        error_messages = {
            "latitude": {"required": "Click the map to drop a pin on the incident location."},
            "longitude": {"required": "Click the map to drop a pin on the incident location."},
        }