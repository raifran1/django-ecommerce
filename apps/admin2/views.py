from django.core.paginator import PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404
from ..produto.models import Product, Category
from ..produto.forms import ProductForm, CategoryForm


def index_admin(request):
    name = 'product_list_admin'
    return render(request, 'admin2/index.html', locals())

def product_list_admin(request):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    products = Product.objects.all()
    paginator = Paginator(products, 2)

    products = paginator.page(page)

    return render(request, 'admin2/list_products.html', locals())

def product_create_admin(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            u = form.save()
            u.save()
            return redirect('product_list_admin')
        else:
            print(form.errors)
    else:
        form = ProductForm()
    return render(request, 'admin2/create_product.html', locals())

def product_detail_admin(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'admin2/detail_product.html', locals())

def product_edit_admin(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            u = form.save()
            u.save()
            return redirect('product_list_admin')
        else:
            print(form.errors)
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin2/edit_product.html', locals())

def product_delete_admin(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.delete()
    return redirect('product_list_admin')


def categories(request):

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    categories = Category.objects.all()
    paginator = Paginator(categories, 2)

    categories = paginator.page(page)

    return render(request, 'admin2/categories.html', locals())

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            u = form.save()
            u.save()
            return redirect('categories')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request, 'admin2/create_category.html', locals())

def category_edit(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            u = form.save()
            u.save()
            return redirect('categories')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin2/create_category.html', locals())

def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('categories')


