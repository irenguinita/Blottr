from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EvidenceUploadForm, IncidentReportForm, ReportFilterForm
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

@login_required(login_url="login:login")
def report_generator(request):
    form = ReportFilterForm(request.GET or None)
    context = {"form": form, "generated": False}

    if request.GET and form.is_valid():
        start = form.cleaned_data["date_from"]
        end = form.cleaned_data["date_to"]
        barangay = form.cleaned_data["barangay"]

        incidents = IncidentReport.objects.select_related(
            "category", "barangay"
        ).filter(
            occurrence_timestamp__date__gte=start,
            occurrence_timestamp__date__lte=end,
        )
        if barangay:
            incidents = incidents.filter(barangay=barangay)

        by_category = list(
            incidents.values("category__category_name")
            .annotate(total=Count("id"))
            .order_by("-total")
        )
        by_barangay = list(
            incidents.values("barangay__name")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        context.update(
            {
                "generated": True,
                "start": start,
                "end": end,
                "barangay": barangay,
                "incidents": incidents.order_by("-occurrence_timestamp"),
                "total": incidents.count(),
                "by_category": by_category,
                "by_barangay": by_barangay,
                "top_category": by_category[0] if by_category else None,
                "top_barangay": by_barangay[0] if by_barangay else None,
                "generated_at": timezone.now(),
            }
        )

    return render(request, "incidents/report.html", context)