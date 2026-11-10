from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Profile


@login_required(login_url="login:login")
def profile_view(request):
    # get_or_create: makes a blank profile the first time a user visits
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.full_name = request.POST.get("full_name", "")
        profile.bio = request.POST.get("bio", "")
        profile.save()
        messages.success(request, "Profile updated.")
        return redirect("user_profile:profile")

    return render(request, "user_profile/profile.html", {"profile": profile})