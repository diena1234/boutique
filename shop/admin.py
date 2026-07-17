from django.contrib import admin
from .models import Category, Product, ProductImage, Order, OrderItem
# en haut du fichier, avec les autres imports
from django.db.models import F, Sum
from django.utils import timezone
from datetime import timedelta

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "old_price", "stock", "is_active", "is_featured")
    list_filter = ("category", "is_active", "is_featured")
    list_editable = ("price", "stock", "is_active", "is_featured")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "unit_price", "quantity")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "city", "status", "total", "created_at")
    list_filter = ("status", "city", "created_at")
    list_editable = ("status",)
    search_fields = ("full_name", "email", "phone")
    inlines = [OrderItemInline]
    readonly_fields = ("user", "full_name", "email", "phone", "address", "city", "notes", "created_at", "updated_at")

# tout en bas de shop/admin.py
def get_dashboard_stats():
    orders = Order.objects.all()
    total_orders = orders.count()
    pending_orders = orders.filter(status=Order.Status.PENDING).count()

    revenue_total = OrderItem.objects.aggregate(
        total=Sum(F("unit_price") * F("quantity"))
    )["total"] or 0

    low_stock_products = Product.objects.filter(stock__lte=5, is_active=True).order_by("stock")[:5]

    top_products = (
        OrderItem.objects.values("product_name")
        .annotate(total_qty=Sum("quantity"), total_revenue=Sum(F("unit_price") * F("quantity")))
        .order_by("-total_qty")[:5]
    )

    today = timezone.now().date()
    chart_labels, chart_data = [], []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_total = OrderItem.objects.filter(order__created_at__date=day).aggregate(
            total=Sum(F("unit_price") * F("quantity"))
        )["total"] or 0
        chart_labels.append(day.strftime("%d/%m"))
        chart_data.append(float(day_total))

    return {
        "stats_total_orders": total_orders,
        "stats_pending_orders": pending_orders,
        "stats_revenue_total": revenue_total,
        "stats_products_count": Product.objects.filter(is_active=True).count(),
        "stats_low_stock_products": low_stock_products,
        "stats_top_products": top_products,
        "stats_chart_labels": chart_labels,
        "stats_chart_data": chart_data,
    }


_original_admin_index = admin.site.index

def _dashboard_index(request, extra_context=None):
    extra_context = extra_context or {}
    extra_context.update(get_dashboard_stats())
    return _original_admin_index(request, extra_context)

admin.site.index = _dashboard_index