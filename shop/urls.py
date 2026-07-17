from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("produits/", views.product_list, name="product_list"),
    path("categorie/<slug:slug>/", views.category_detail, name="category_detail"),
    path("produit/<slug:slug>/", views.product_detail, name="product_detail"),
    path("panier/", views.cart_detail, name="cart_detail"),
    path("panier/ajouter/<int:product_id>/", views.cart_add, name="cart_add"),
    path("panier/retirer/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("panier/modifier/<int:product_id>/", views.cart_update, name="cart_update"),
    path("commande/", views.checkout, name="checkout"),
    path("commande/succes/<int:order_id>/", views.order_success, name="order_success"),
    path("mes-commandes/", views.order_history, name="order_history"),
]
