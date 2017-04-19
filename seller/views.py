from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import edit

from seller.forms.packsForms import PackForm
from seller.models import Product, Local, Category, Pack, ProductLine
from django.shortcuts import get_list_or_404, render_to_response, render, redirect, get_object_or_404

from forms.forms import LocalForm, CategoryForm, ProductForm

from forms.forms import LocalForm
from bocatapp.decorators import permission_required
from customer.models import Order
from customer.services import CommentService


# Create your views here.

# Lista el menu de productos de un local
def menu_list(request, pk):
    local = get_list_or_404(Local, id=pk)[0]
    productos = local.product_set.all()
    return render(request, 'menu.html',
                  {'productos': productos, 'local': local})


# Lista las categorias de un local
def category_list(request, pk):
    categories = get_list_or_404(Category, local=pk)
    return render(request, 'category_list.html',
                  {'categories': categories})


def product_list_category(request, pk):
    productos = get_list_or_404(Product, category=pk)
    return render(request, 'menu.html',
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
        # aqui se comprueba que el vendedor es el que esta logueado
        if form.is_valid() and category.local.seller == request.user:
            category = form.save(commit=False)
            category.save()
            return redirect('seller.views.category_list', pk=category.local.pk)
    else:
        form = CategoryForm(instance=category)

    return render(request, 'category_edit.html', {'form': form, 'locals': locals})


# Vista para la creacion de un nuevo producto

def product_new(request, pk):
    local = get_object_or_404(Local, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, pk=pk)
        if form.is_valid() and local.seller == request.user:
            product = form.createProduct()
            product.local = local
            product.save()
            return redirect('menu_list', pk=product.local.id)
    else:
        form = ProductForm(pk=pk)

    return render(request, 'product_edit.html', {'form': form})


# Listado de locales dado un seller
def get_my_locals(request, pk):
    locals = get_list_or_404(Local, seller=pk)
    return render(request, 'local_list.html',
                  {'locals': locals})


# Vista para el lisstado de locales
def local_list(request):
    locals = Local.objects.all()
    ratings = []
    for local in locals:
        ratings.append(CommentService.get_stars(local.pk))

    ratings.reverse()

    return render(request, 'local_list.html', {'locals': locals,'ratings': ratings})


def local_orders(request, pk):
    orders = get_list_or_404(Order, local=pk)
    return render(request, 'orders.html', {'orders': orders})


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
    ratings = []
    for local in locals:
        ratings.append(CommentService.get_stars(local.pk))

    ratings.reverse()

    return render(request, 'cp_search.html', {'locals': locals,'ratings': ratings})


# Packs--------------------------------------------------------------------------
def packs_list(request):
    packs = get_list_or_404(Pack)
    return render(request, 'pack/list.html',
                  {'packs': packs})


def local_packs(request, local_pk):
    packs = Local.objects.get(id=local_pk).pack_set.all()
    local = Local.objects.get(id=local_pk)
    return render(request, 'pack/list.html',
                  {'packs': packs, 'local': local})


def pack_details(request, pk):
    pack = get_object_or_404(Pack, id=pk)
    return render(request, 'pack/details.html',
                  {'pack': pack})


class EditPack(edit.View):
    # @permission_required('bocatapp.seller', message='You are not a seller')
    def get(self, request, local_pk):
        pack_form = PackForm()
        local_products = get_object_or_404(Local, id=local_pk).product_set.all()
        context = {
            'pack_form': pack_form,
            'local_products': local_products,
            'local_pk': local_pk
        }
        return render(request, 'pack/edit.html', context)

        # @permission_required('bocatapp.seller', message='You are not a seller')

    @transaction.atomic
    def post(self, request, local_pk):
        if request.user.is_authenticated():
            pack_form = PackForm(request.POST)
            local_products = get_object_or_404(Local, id=local_pk).product_set.all()
            if pack_form.is_valid():
                pack = pack_form.create(local_pk)
                pack.save()

                for product in local_products:
                    quantity = request.POST.get(str(product.id))
                    if quantity and int(quantity) > 0:
                        product_line = ProductLine(quantity=int(quantity), product=product, pack=pack)
                        product_line.save()
                return redirect('local_packs', local_pk=local_pk)
            else:
                message = ""
                for field, errors in pack_form.errors.items():
                    for error in errors:
                        message += error

                return render(request, 'pack/edit.html', {
                    'local_pk': local_pk, 'pack_form': pack_form, 'local_products': local_products, 'message': message})

        else:
            return render(request, '../templates/forbidden.html')
