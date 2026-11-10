from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from apps.incidents.models import IncidentReport


@login_required(login_url="login:login")
def home_view(request):
    today = timezone.localdate()
    context = {
        "today_count": IncidentReport.objects.filter(occurrence_timestamp__date=today).count(),
        "open_count": IncidentReport.objects.filter(status="open").count(),
        "investigating_count": IncidentReport.objects.filter(status="under_investigation").count(),
        "total_count": IncidentReport.objects.count(),
        "recent": IncidentReport.objects.select_related("category")[:5],
    }
    return render(request, "home/home.html", context)