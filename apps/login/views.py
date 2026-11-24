"""
LOGIN feature — owns all authentication-related behavior.
Per the vertical slicing rule: login logic stays here, not in Home.
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme


def _safe_next(request, value):
    """Return `value` only if it points to this site, else an empty string."""
    if value and url_has_allowed_host_and_scheme(
        value,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return value
    return ""


def login_view(request):
    next_url = _safe_next(request, request.POST.get("next") or request.GET.get("next"))

    if request.user.is_authenticated:
        return redirect(next_url or "home:home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url or "home:home")
        return render(request, "login/login.html", {
            "error": "Invalid username or password.",
            "next": next_url,
        })
    return render(request, "login/login.html", {"next": next_url})


@login_required(login_url="login:login")
def logout_view(request):
    logout(request)
    return redirect("login:login")