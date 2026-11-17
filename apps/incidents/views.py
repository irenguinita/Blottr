from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EvidenceUploadForm, IncidentReportForm
from .models import EvidenceFile, IncidentCategory, IncidentReport

DEFAULT_CATEGORIES = [
    "Theft", "Robbery", "Assault", "Vandalism", "Traffic Accident",
    "Public Disturbance", "Domestic Dispute", "Missing Person", "Other",
]


def _ensure_categories():
    # First visit: fill the category list so the dropdown isn't empty
    if not IncidentCategory.objects.exists():
        IncidentCategory.objects.bulk_create(
            [IncidentCategory(category_name=n) for n in DEFAULT_CATEGORIES]
        )


@login_required(login_url="login:login")
def incident_create(request):
    _ensure_categories()
    if request.method == "POST":
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, "Incident recorded successfully.")
            return redirect("incidents:list")
    else:
        form = IncidentReportForm()
    return render(request, "incidents/incident_form.html", {"form": form})


@login_required(login_url="login:login")
def incident_list(request):
    reports = IncidentReport.objects.select_related("category", "barangay", "user")[:50]
    return render(request, "incidents/incident_list.html", {"reports": reports})


@login_required(login_url="login:login")
def incident_map(request):
    reports = IncidentReport.objects.select_related("category")
    points = [
        {
            "lat": r.latitude,
            "lng": r.longitude,
            "cat": r.category.category_name,
            "when": r.occurrence_timestamp.strftime("%b %d, %Y %I:%M %p"),
        }
        for r in reports
    ]
    categories = IncidentCategory.objects.all()
    return render(
        request,
        "incidents/incident_map.html",
        {"points": points, "categories": categories},
    )

@login_required(login_url="login:login")
def evidence_vault(request, pk):
    report = get_object_or_404(
        IncidentReport.objects.select_related("category", "barangay"), pk=pk
    )
    if request.method == "POST":
        form = EvidenceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for f in form.cleaned_data["files"]:
                EvidenceFile.objects.create(
                    report=report,
                    file=f,
                    original_name=f.name,
                    uploaded_by=request.user,
                )
            messages.success(request, "Evidence uploaded successfully.")
            return redirect("incidents:evidence", pk=report.pk)
    else:
        form = EvidenceUploadForm()

    return render(
        request,
        "incidents/evidence_vault.html",
        {"report": report, "form": form, "files": report.evidence_files.all()},
    )