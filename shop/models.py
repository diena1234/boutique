from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Catégorie d'accessoires : Bijoux, Coques de téléphone, Chaussures, etc."""
    name = models.CharField("Nom", max_length=100)
    slug = models.SlugField("Slug", max_length=120, unique=True, blank=True)
    description = models.TextField("Description", blank=True)
    image = models.ImageField("Image", upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:category_detail", args=[self.slug])


class Product(models.Model):
    """Un produit : bijou, coque de téléphone, chaussure, etc."""
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE, verbose_name="Catégorie"
    )
    name = models.CharField("Nom", max_length=200)
    slug = models.SlugField("Slug", max_length=220, unique=True, blank=True)
    description = models.TextField("Description", blank=True)
    price = models.DecimalField("Prix (FCFA)", max_digits=10, decimal_places=0)
    old_price = models.DecimalField(
        "Ancien prix (FCFA)", max_digits=10, decimal_places=0, blank=True, null=True,
        help_text="Facultatif : à renseigner pour afficher une promotion."
    )
    stock = models.PositiveIntegerField("Stock disponible", default=0)
    image = models.ImageField("Image principale", upload_to="products/", blank=True, null=True)
    is_active = models.BooleanField("Actif / visible", default=True)
    is_featured = models.BooleanField("Mis en avant", default=False)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            i = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base_slug}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.slug])

    @property
    def is_on_sale(self):
        return bool(self.old_price and self.old_price > self.price)

    @property
    def discount_percent(self):
        if self.is_on_sale:
            return round((1 - (self.price / self.old_price)) * 100)
        return 0

    @property
    def in_stock(self):
        return self.stock > 0


class ProductImage(models.Model):
    """Images supplémentaires pour un produit (galerie)."""
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField("Image", upload_to="products/gallery/")
    alt_text = models.CharField("Texte alternatif", max_length=200, blank=True)

    class Meta:
        verbose_name = "Image produit"
        verbose_name_plural = "Images produit"

    def __str__(self):
        return f"Image de {self.product.name}"


class Order(models.Model):
    """Commande passée par un client."""

    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        CONFIRMED = "confirmed", "Confirmée"
        SHIPPED = "shipped", "Expédiée"
        DELIVERED = "delivered", "Livrée"
        CANCELLED = "cancelled", "Annulée"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="Client"
    )
    full_name = models.CharField("Nom complet", max_length=200)
    email = models.EmailField("Email")
    phone = models.CharField("Téléphone", max_length=30)
    address = models.CharField("Adresse", max_length=255)
    city = models.CharField("Ville", max_length=100, default="Dakar")
    notes = models.TextField("Notes / instructions", blank=True)
    status = models.CharField(
        "Statut", max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField("Créée le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifiée le", auto_now=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Commande #{self.pk} - {self.full_name}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    """Ligne de commande."""
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.SET_NULL, null=True
    )
    product_name = models.CharField("Nom du produit", max_length=200)
    unit_price = models.DecimalField("Prix unitaire", max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField("Quantité", default=1)

    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    @property
    def subtotal(self):
        return self.unit_price * self.quantity
