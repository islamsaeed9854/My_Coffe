from gc import is_finalized
from logging import exception
from multiprocessing import context
import re
from tkinter import S
from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from orders.models import Order, OrderDetails
from django.utils import timezone
from products.views import product
from .models import Payment
# Create your views here.


def get_title(request):
    path = request.path
    if path[len(path)-1] == '/':
        path = path[:-1]
    path = path[::-1]
    tit = ""
    for i in path:
        if i == '/':
            break
        tit = tit + i
    tit = tit[::-1]
    return tit


def add_to_card(request):
    if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET \
            and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id = request.GET['pro_id']
        qty = request.GET['qty']
        price = request.GET['price']
        order = Order.objects.all().filter(user=request.user, is_finished=False)
        if Product.objects.all().filter(id=pro_id):
            pro = Product.objects.get(id=pro_id)
        else:
            return redirect("products")
        if order:
            old_order = Order.objects.get(user=request.user, is_finished=False)
            if OrderDetails.objects.all().filter(order=old_order, product=pro):
                orderdetails = OrderDetails.objects.all().get(order=old_order, product=pro)
                orderdetails.quantity += int(qty)
                orderdetails.quantity = max(orderdetails.quantity, 1)
                orderdetails.save()
            else:
                orderdetails = OrderDetails.objects.create(
                    product=pro, order=old_order, price=pro.price, quantity=qty)
            messages.success(request, "added to cart for old order")
        else:
            new_order = Order()
            new_order.user = request.user
            new_order.is_finished = False
            new_order.order_date = timezone.now()
            new_order.save()
            orderdetails = OrderDetails.objects.create(
                product=pro, order=new_order, price=pro.price, quantity=qty)
            messages.success(request, "was added to cart for new order")
        return redirect("/products" + str(pro_id))
    else:
        if 'pro_id' in request.GET:
            messages.error(request,  'you must be logged in')
            return redirect("/products" + request.GET['pro_id'])
        else:
            return redirect("index")


def cart(request):
    context = {
        'tit': get_title(request),
        'orderdatails': None,
        'total': None,
        'order': None,
    }
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user, is_finished=False):
            order = Order.objects.all().get(user=request.user, is_finished=False)
            orderdatails = OrderDetails.objects.all().filter(order=order)
            total = 0
            for sub in orderdatails:
                total += sub.price*sub.quantity
            context['orderdatails'] = orderdatails
            context['total'] = total
            context['order'] = order
    return render(request, "orders/cart.html", context)


def remove_from_cart(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        if Order.objects.all().filter(user=request.user, is_finished=False):
            order_id = Order.objects.all().get(user=request.user, is_finished=False)
            od = OrderDetails.objects.all().filter(id=orderdetails_id, order_id=order_id)
            od.delete()
    return redirect("cart")


def add_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.all().get(id=orderdetails_id)
        orderdetails.quantity += 1
        orderdetails.save()
    return redirect("cart")


def sub_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.all().get(id=orderdetails_id)
        if orderdetails.quantity > 1:
            orderdetails.quantity -= 1
            orderdetails.save()
    return redirect("cart")


def payment(request):
    if request.method == 'POST' and "btnpayment" in request.POST \
            and 'ship_address' in request.POST and 'ship_phone' in request.POST \
            and 'card_number' in request.POST and 'expire' in request.POST \
            and 'security_code' in request.POST:
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user, is_finished=False):
                order = Order.objects.all().get(user=request.user, is_finished=False)
                ship_address = request.POST['ship_address']
                ship_phone = request.POST['ship_phone']
                card_number = request.POST['card_number']
                expire = request.POST['expire']
                security_code = request.POST['security_code']
                is_added = True
                context = {
                    'tit': get_title(request),
                    'ship_address': ship_address,
                    'ship_phone': ship_phone,
                    'expire': expire,
                    'security_code': security_code,
                    'is_added': is_added
                }
                payment = Payment(order=order, shipment_address=ship_address, shipment_phone=ship_phone,
                                  card_number=card_number,  expire=expire, security_code=security_code)
                payment.save()
                order.is_finished = True
                order.save()
                messages.success(request, "Your order is finished")
        return redirect("payment")
    else:
        context = {
            'tit': get_title(request),
            'orderdatails': None,
            'total': None,
            'order': None,
        }
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user, is_finished=False):
                order = Order.objects.all().get(user=request.user, is_finished=False)
                orderdatails = OrderDetails.objects.all().filter(order=order)
                total = 0
                for sub in orderdatails:
                    total += sub.price*sub.quantity
                if total > 0:
                    context['orderdatails'] = orderdatails
                    context['total'] = total
                    context['order'] = order
    return render(request, 'orders/payment.html', context)


def show_orders(request):
    context = None
    all_orders = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user=request.user)
        if all_orders:
            for x in all_orders:
                order = Order.objects.all().get(id=x.id)
                orderdatails = OrderDetails.objects.all().filter(order=order)
                total = 0
                for sub in orderdatails:
                    total += sub.price*sub.quantity
                x.total = total
                x.count = orderdatails.count
        context = {
            'all_orders': all_orders,
            'tit': get_title(request),
        }
    return render(request, 'orders/show_orders.html', context)
