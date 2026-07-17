from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import SignUpForm, StyledAuthenticationForm


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = StyledAuthenticationForm


class CustomLogoutView(LogoutView):
    next_page = "shop:home"


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("shop:home")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})
