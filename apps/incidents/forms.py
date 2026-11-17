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
            "barangay",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["barangay"].required = True
        self.fields["barangay"].empty_label = "Select barangay"

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_clean(d, initial) for d in data]
        return [single_clean(data, initial)]


class EvidenceUploadForm(forms.Form):
    ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf", ".doc", ".docx")
    MAX_SIZE_MB = 10

    files = MultipleFileField(label="Evidence files")

    def clean_files(self):
        files = self.cleaned_data["files"]
        for f in files:
            if not f.name.lower().endswith(self.ALLOWED_EXTENSIONS):
                raise forms.ValidationError(
                    f"'{f.name}' is not an allowed file type "
                    "(images, PDF, or Word documents only)."
                )
            if f.size > self.MAX_SIZE_MB * 1024 * 1024:
                raise forms.ValidationError(
                    f"'{f.name}' is larger than {self.MAX_SIZE_MB} MB."
                )
        return files