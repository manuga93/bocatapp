from django.http import HttpResponse
from seller.models import Product, Local
from django.shortcuts import get_list_or_404, render_to_response, render, redirect, get_object_or_404
from forms.forms import LocalForm
from bocatapp.decorators import permission_required


# Create your views here.

def carta(request):  # Recibira una id de local def carta(request, local_id)
    productos = Product.objects.all()  # productos = get_list_or_404(Producto, fk=local_id)
    return render_to_response('carta.html',
                              {'productos': productos})


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
