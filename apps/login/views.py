"""
LOGIN feature — owns all authentication-related behavior.
Per the vertical slicing rule: login logic stays here, not in Home.
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home:home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home:home")
        return render(request, "login/login.html", {
            "error": "Invalid username or password."
        })
    return render(request, "login/login.html")


@login_required(login_url="login:login")
def logout_view(request):
    logout(request)
    return redirect("login:login")
