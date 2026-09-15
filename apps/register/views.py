"""
REGISTER feature — owns account creation. Kept separate from Login,
even though both touch the User model, because they're different
business capabilities (create vs. authenticate).
"""
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "register/register.html", {
                "error": "Passwords do not match."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "register/register.html", {
                "error": "Username already exists."
            })

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created! You can now log in.")
        return redirect("login:login")

    return render(request, "register/register.html")
