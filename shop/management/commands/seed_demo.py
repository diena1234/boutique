from django.core.management.base import BaseCommand
from shop.models import Category, Product


CATALOG = {
    "Bijoux": [
        ("Collier Perle Dorée", 8500, None),
        ("Bracelet Chaîne Fine", 5000, 6500),
        ("Boucles d'oreilles Créoles", 4000, None),
        ("Bague Signet Argentée", 6000, None),
    ],
    "Coques de téléphone": [
        ("Coque Silicone iPhone 15", 4500, None),
        ("Coque Transparente Renforcée", 3500, None),
        ("Coque Paillettes Samsung", 4000, 5000),
        ("Coque Cuir Premium", 7000, None),
    ],
    "Chaussures": [
        ("Sneakers Blanches Unisexe", 15000, 18000),
        ("Sandales Été Femme", 9000, None),
        ("Mocassins Cuir Homme", 17500, None),
        ("Baskets Running Léger", 20000, None),
    ],
    "Sacs & Accessoires": [
        ("Sac à Main Bandoulière", 12000, 14500),
        ("Ceinture Cuir Réversible", 6500, None),
        ("Lunettes de Soleil Tendance", 5500, None),
        ("Montre Minimaliste", 13000, None),
    ],
}


class Command(BaseCommand):
    help = "Crée des catégories et produits de démonstration (sans images)."

    def handle(self, *args, **options):
        for cat_name, products in CATALOG.items():
            category, created = Category.objects.get_or_create(name=cat_name)
            self.stdout.write(f"Catégorie: {cat_name} ({'créée' if created else 'existante'})")
            for name, price, old_price in products:
                product, created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        "category": category,
                        "price": price,
                        "old_price": old_price,
                        "stock": 25,
                        "description": f"{name} — article de la collection {cat_name}, disponible en édition limitée.",
                        "is_featured": old_price is not None,
                    },
                )
                if created:
                    self.stdout.write(f"  + {name}")
        self.stdout.write(self.style.SUCCESS("Données de démonstration créées avec succès."))
