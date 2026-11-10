from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserSettings


@login_required(login_url="login:login")
def settings_view(request):
    user_settings, _ = UserSettings.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # A checkbox only appears in POST when it is ticked
        user_settings.dark_mode = "dark_mode" in request.POST
        user_settings.email_notifications = "email_notifications" in request.POST
        user_settings.save()
        messages.success(request, "Settings saved.")
        return redirect("user_settings:settings")

    return render(request, "user_settings/settings.html", {"s": user_settings})