
from django.shortcuts import render_to_response, get_object_or_404,get_list_or_404, redirect, render
from customer.services import OrderService
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from customer.models import Order, OrderLine, Comment, Report
from forms.forms import CommentForm, ReportForm
from seller.models import Local
from bocatapp.decorators import permission_required
from customer.services import ReportService



# Create your views here.

# This method is for testing the funcionality


def all_orders(request):
    try:
        orders = OrderService.find_all_orders()
        return render_to_response('orders.html', {'orders': orders}, context_instance=RequestContext(request))
    except Order.DoesNotExist:
        return render_to_response('error.html', context_instance=RequestContext(request))


def order_line_by_order(request, order_id):
    try:
        orders_line = OrderService.find_order_line_by_order(order_id)
        return render_to_response('ordersLine.html', {'lines': orders_line}, context_instance=RequestContext(request))
    except OrderLine.DoesNotExist:
        return render_to_response('error.html', context_instance=RequestContext(request))


def do_order_line(request, id1):
    order_line = get_object_or_404(OrderLine, pk=id1)
    order_line.status = True
    order_line.save()
    OrderService.set_order_status(order_line.order_id)
    return HttpResponseRedirect("/customer/ordersLine/" + str(order_line.order_id))

@permission_required('bocatapp.customer', message='You are not a customer')
def comment_new(request, pk):
    local = get_object_or_404(Local, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.local = local
            comment.customer = request.user

            comment.save()
            return redirect('seller.views.local_detail', pk=local.pk)
    else:
        form = CommentForm()

    return render(request, 'comment_edit.html', {'form': form})

@permission_required('bocatapp.customer', message='You are not a customer')
def report_new(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.comment = comment

            report.save()
            return redirect('seller.views.local_detail', pk=comment.local.pk)
    else:
        form = ReportForm()

    return render(request, 'comment_edit.html', {'form': form})


# Lista los comentarios de un local
def comment_list(request, pk):
    comentarios = Comment.objects.filter(local = pk, reported=0)
    return render_to_response('comment_list.html',
                                {'comentarios': comentarios,'local':pk})

# Lista los reportes de un comentario
@permission_required('bocatapp.administrator', message='You are not an administrator')
def report_list(request, pk):
    reports = Report.objects.filter(comment = pk, accepted=0,decline=0)
    return render_to_response('report_list.html',
                                {'reports': reports})

@permission_required('bocatapp.administrator', message='You are not an administrator')
def report_accept(request, pk):
    ReportService.accept_report(pk)
    report = get_object_or_404(Report, pk=pk)
    return redirect('seller.views.local_detail', pk=report.comment.local.pk)

@permission_required('bocatapp.administrator', message='You are not an administrator')
def report_decline(request, pk):
    ReportService.decline_report(pk)
    report = get_object_or_404(Report, pk=pk)
    return redirect('customer.views.report_list', pk=report.comment.pk)