"""
Views for the products application.
"""
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Product, ProductCategory, ProductManufacturer


def product_list(request):
    """Display product catalog with filtering and search."""
    products = Product.objects.filter(is_active=True).select_related(
        'category', 'manufacturer'
    ).prefetch_related('images')
    
    # Search
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(part_number__icontains=search) |
            Q(manufacturer_part_number__icontains=search) |
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Filter by manufacturer
    manufacturer_id = request.GET.get('manufacturer')
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)

    # Lifecycle status (ACTIVE / DISCONTINUED)
    status = request.GET.get("status")
    if status:
        products = products.filter(status=status)

    # Inventory (derived)
    stock = request.GET.get("stock")
    if stock == "in":
        products = products.filter(quantity_in_stock__gt=0)
    elif stock == "out":
        products = products.filter(quantity_in_stock=0)

    # Pagination
    paginator = Paginator(products, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': ProductCategory.objects.filter(is_active=True),
        'manufacturers': ProductManufacturer.objects.filter(is_active=True),
    }

    if request.headers.get("HX-Request"):
        return render(
            request,
            "products/_product_results.html",
            context,
        )

    return render(
        request,
        "products/product_list.html",
        context,
    )


@login_required
def customer_catalog(request):
    """Customer-specific catalog view."""
    return product_list(request)


def product_detail(request, slug):
    """Display detailed product information."""
    product = get_object_or_404(
        Product.objects.select_related('category', 'manufacturer').prefetch_related(
            'images', 'documents', 'vehicle_applications__make', 
            'vehicle_applications__model', 'attributes'
        ),
        slug=slug,
        is_active=True
    )
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)
