from django.http import HttpResponse

from seller.models import Product, Local, Category
from django.shortcuts import get_list_or_404, render_to_response, render, redirect, get_object_or_404

from forms.forms import LocalForm, CategoryForm, ProductForm

from forms.forms import LocalForm
from bocatapp.decorators import permission_required

# Create your views here.

# Lista el menu de productos de un local
def menu_list(request, local_id): 
    productos = get_list_or_404(Product, local_pk = local_id) 
    return render_to_response('carta.html', 
                                {'productos': productos})

# Vista para la creacion de una nueva categoria

def category_new(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('seller.views.local_new')
    else:
        form = CategoryForm()
        
    return render(request, 'category_edit.html', {'form': form})

# Vista para la creacion de un nuevo producto (a falta de seleccionar el local)

def product_new(request):
    
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('seller.views.local_new')
    else:
        form = ProductForm()

    return render(request, 'product_edit.html', {'form': form})

# Vista para el listado de categorias y productos

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

# Vista para el lisstado de locales
@permission_required('bocatapp.customer', message='you cant enter')
def local_list(request):
    locals = Local.objects.all()
    return render(request, 'local_list.html', {'locals': locals})


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
