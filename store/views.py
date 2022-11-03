from django.shortcuts import render, HttpResponseRedirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse


def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        s_image = HomepageSlideshow.objects.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        s_image = HomepageSlideshow.objects.all()
    contex = {'items': items,'order':order,'cartItems':cartItems,'images':s_image}
    return render(request,'home.html',contex)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
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
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    category = Category.get_all_category()
    products = None
    categoryID= request.GET.get('category')

    if categoryID:
        products = Product.get_all_product_by_category_id(categoryID)
    else:
        products = Product.get_all_products()

    contex = {'items': items,'products':products,'cartItems':cartItems,'order':order,'category':category}
    return render(request,'shop.html',contex)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()

        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
    contex = {'items': items,'order': order,'cartItems': cartItems}
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


def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        OrderDetail.objects.create(
            customer=customer,
            order=order,
            mobile=data['form']['mobile'],
            emailaddress=data['form']['email'],
            address=data['form']['address'],
        )

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        template = render_to_string('store/order.html',{'name':request.user.username})
        subject = 'Order Confirmations'
        # body = 'Your Account is Activated'
        from_mail = settings.EMAIL_HOST_USER
        to_mail = [request.user.email]
        send_mail(
            subject,
            # body,
            template,
            from_mail,
            to_mail,
        )
        send_mail(subject, template, from_mail, to_mail, fail_silently=False)

    else:
        print('user is not logged in ')

    return JsonResponse('Payment Done .. ', safe=False)


def view_details(request,id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        cartItems = order.get_cart_items
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
    details = Product.objects.get(pk = id)
    contex = {'details':details,'cartItems':cartItems,'items':items}
    return render(request,'details.html',contex)

def price(request):
    if request.user.is_authenticated:
        context= {}
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer, complete = True).values()
        context['total_order'] = len(orders)
        if orders:
            items = []
            for x in orders:
                order_items = OrderItem.objects.filter(order = x.get("id")).values()
                for or_itms in order_items:
                    data_dict = {}
                    item = Product.objects.get(id = or_itms.get("product_id"))
                    data_dict["item_name"] = item.name
                    data_dict["qty"] = or_itms.get("quantity")
                    data_dict["order"] = x.get("id")
                    items.append(data_dict)
            context["items"] = items
        print(context)
    return render(request,'user_order_details.html',context)