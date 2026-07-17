from .cart import Cart
from .models import Category


def cart(request):
    """Rend le panier et la liste des catégories disponibles dans tous les templates
    (utilisé pour le badge du panier et le menu de navigation)."""
    return {
        "cart": Cart(request),
        "nav_categories": Category.objects.all(),
    }
