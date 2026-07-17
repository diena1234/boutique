from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("inscription/", views.signup, name="signup"),
    path("connexion/", views.CustomLoginView.as_view(), name="login"),
    path("deconnexion/", views.CustomLogoutView.as_view(), name="logout"),
]
