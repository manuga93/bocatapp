from django.http import HttpResponse

from seller.models import Product, Local, Category
from django.shortcuts import get_list_or_404, render_to_response, render, redirect, get_object_or_404

from forms.forms import LocalForm, CategoryForm, ProductForm

from forms.forms import LocalForm
from bocatapp.decorators import permission_required
from customer.models import Order

# Create your views here.

# Lista el menu de productos de un local
def menu_list(request, pk):
    productos = get_list_or_404(Product, local = pk)
    return render(request, 'carta.html',
                                {'productos': productos})

# Lista las categorias de un local
def category_list(request, pk):
    categories = get_list_or_404(Category, local=pk)
    return render(request, 'category_list.html',
                                {'categories': categories})

def product_list_category(request, pk):
    productos = get_list_or_404(Product, category = pk)
    return render(request, 'carta.html',
                                {'productos': productos})

# Vista para la creacion de una nueva categoria

def category_new(request, pk):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        local = get_object_or_404(Local, pk=pk)
        if form.is_valid():
            category = form.save(commit=False)
            category.local = local
            category.save()
            return redirect('/')
    else:
        form = CategoryForm()

    return render(request, 'category_edit.html', {'form': form})

# Editar una categoria
@permission_required('bocatapp.seller', message='You are not a seller')
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        #aqui se comprueba que el vendedor es el que esta logueado
        if form.is_valid() and category.local.seller == request.user:
            category = form.save(commit=False)
            category.save()
            return redirect('seller.views.category_list', pk=category.local.pk)
    else:
        form = CategoryForm(instance=category)

    return render(request, 'category_edit.html', {'form': form, 'locals': locals})


# Vista para la creacion de un nuevo producto

def product_new(request):

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('menu_list', pk = product.local.id)
    else:
        form = ProductForm()

    return render(request, 'product_edit.html', {'form': form})

#Listado de locales dado un seller

def get_my_locals(request, pk):
    locals = get_list_or_404(Local, seller=pk)
    return render(request, 'local_list.html',
                                {'locals': locals})


# Vista para el lisstado de locales
def local_list(request):
    locals = Local.objects.all()
    return render(request, 'local_list.html', {'locals': locals})

def local_orders(request, pk):
    orders = get_list_or_404(Order, local=pk)
    return render(request, 'orders.html' ,{'orders': orders})

# Vista para la creacion de un nuevo local
@permission_required('bocatapp.seller', message='You are not a seller')
def local_new(request):
    if request.method == "POST":
        form = LocalForm(request.POST)
        if form.is_valid():
            local = form.save(commit=False)
            local.seller = request.user
            local.isActive = True
            local.save()
            return redirect('seller.views.local_detail', pk=local.pk)
    else:
        form = LocalForm()

    return render(request, 'local_edit.html', {'form': form})


# Vista para los detalles de un local
def local_detail(request, pk):
    local = get_object_or_404(Local, pk=pk)
    return render(request, 'local_detail.html', {'local': local})


# Vista para la creacedicion de un local
def local_edit(request, pk):
    local = get_object_or_404(Local, pk=pk)
    if request.method == "POST":
        form = LocalForm(request.POST, instance=local)
        if form.is_valid():
            local = form.save(commit=False)
            local.seller = request.user
            local.isActive = True
            local.save()
            return redirect('seller.views.local_detail', pk=local.pk)
    else:
        form = LocalForm(instance=local)

    return render(request, 'local_edit.html', {'form': form})


def search(request):
    # TODO: This is not finished!
    locals = Local.objects.all()
    return render(request, 'cp_search.html', {'locals': locals})
