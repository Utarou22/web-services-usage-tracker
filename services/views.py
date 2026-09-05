from django.shortcuts import render

from .models import Service

def dashboard(request):
    services = Service.objects.select_related("provider").prefetch_related("plans")

    return render(
        request,
        "services/dashboard.html",
        {"services": services},
    )