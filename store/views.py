from django.shortcuts import render, HttpResponseRedirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,logout,login

def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = 0
    contex = {'items': items,'order':order,'cartItems':cartItems}
    return render(request,'home.html',contex)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = 0
    contex = {'items': items,'order':order,'cartItems':cartItems}
    return render(request,'cart.html',contex)

def shop(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:

        cartItems = 0
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

    products = Product.objects.all()
    contex = {'items': items,'products':products,'cartItems':cartItems,'order':order}
    return render(request,'shop.html',contex)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()

        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = 0
    contex = {'items': items,'order':order,'cartItems':cartItems}
    return render(request,'checkout.html',contex)

def update_item(request):

    data = json.loads(request.body)
    productId = int(data['productId'])
    action = data['action']


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item is added', safe=False)

def sign_in(request):
    cartItems = 0

    if request.method == 'POST':

        form = UserCreationForm(request=request,data=request.POST)

        if form.is_valid():
            form.save()
            form = UserCreationForm()
    else:
        form = UserCreationForm()
    contex = {'form':form,'cartItems':cartItems}
    return render(request,'signin.html',contex)

def log_in(request):
    cartItems = 0
    if request.method == 'POST':
        form = AuthenticationForm(request = request, data=request.POST)
        if form.is_valid():

            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']

            user = authenticate(username = uname , password = upass)

            if user is not None :
                login(request,user)
                return HttpResponseRedirect('/')


    form = AuthenticationForm()
    contex = {'form':form,'cartItems':cartItems}
    return render(request,'login.html',contex)

def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        OrderDetail.objects.create(
            customer=customer,
            order=order,
            mobile=data['form']['mobile'],
            emailaddress=data['form']['email'],
            address =data['form']['address'],
        )

    else:
        print('user is not logged in ')

    return JsonResponse('Payment Done .. ', safe=False)


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/log_in/')


def view_details(request,id):
    details = Product.objects.get(pk = id)
    contex = {'details':details}
    return render(request,'details.html',contex)