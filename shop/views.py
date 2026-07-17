from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .cart import Cart
from .forms import AddToCartForm, CheckoutForm
from .models import Category, Order, OrderItem, Product


def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    latest_products = Product.objects.filter(is_active=True)[:8]
    return render(request, "shop/home.html", {
        "categories": categories,
        "featured_products": featured_products,
        "latest_products": latest_products,
    })


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    category_slug = request.GET.get("categorie")
    query = request.GET.get("q")

    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    sort = request.GET.get("tri")
    if sort == "prix_asc":
        products = products.order_by("price")
    elif sort == "prix_desc":
        products = products.order_by("-price")
    elif sort == "recent":
        products = products.order_by("-created_at")

    return render(request, "shop/product_list.html", {
        "products": products,
        "categories": categories,
        "current_category": current_category,
        "query": query or "",
        "sort": sort or "",
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return redirect(f"/produits/?categorie={category.slug}")


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]
    form = AddToCartForm()
    return render(request, "shop/product_detail.html", {
        "product": product,
        "related_products": related_products,
        "form": form,
    })


def cart_detail(request):
    cart = Cart(request)
    return render(request, "shop/cart_detail.html", {"cart": cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    if request.method == "POST":
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart.add(product=product, quantity=form.cleaned_data["quantity"])
            messages.success(request, f"« {product.name} » a été ajouté au panier.")
    else:
        cart.add(product=product, quantity=1)
        messages.success(request, f"« {product.name} » a été ajouté au panier.")
    return redirect("shop:cart_detail")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"« {product.name} » a été retiré du panier.")
    return redirect("shop:cart_detail")


def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity < 1:
            cart.remove(product)
        else:
            cart.add(product=product, quantity=quantity, override_quantity=True)
    return redirect("shop:cart_detail")


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Votre panier est vide.")
        return redirect("shop:product_list")

    initial = {}
    if request.user.is_authenticated:
        initial = {
            "full_name": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
        }

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    product_name=item["product"].name,
                    unit_price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            messages.success(request, "Votre commande a bien été enregistrée !")
            return redirect("shop:order_success", order_id=order.id)
    else:
        form = CheckoutForm(initial=initial)

    return render(request, "shop/checkout.html", {"cart": cart, "form": form})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "shop/order_success.html", {"order": order})


@login_required
def order_history(request):
    orders = request.user.orders.all()
    return render(request, "shop/order_history.html", {"orders": orders})
