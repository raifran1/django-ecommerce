from django.core.paginator import PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from ..produto.models import Product, Category


def products(request):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    products = Product.objects.all()
    paginator = Paginator(products, 6)

    products = paginator.page(page)

    return render(request, 'produto/products.html', locals())


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'produto/product.html', locals())

def category_detail(request, id):
    category = get_object_or_404(Category, id=id)

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    products = Product.objects.filter(category=category)
    paginator = Paginator(products, 6)

    products = paginator.page(page)

    return render(request, 'produto/products.html', locals())