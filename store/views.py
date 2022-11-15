from django.shortcuts import render, HttpResponseRedirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404


def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        if customer:
            order_items = OrderItem.objects.filter(~Q(order=order.id)).values().order_by("-date_added")[:15]
            items = []
            for x in order_items:
                item = Product.objects.get(id = x.get("product_id"))
                data_dict = {'name':item.name,'image':item.imagesURL,'price':item.price,'id':item.id}
                items.append(data_dict)
    else:
        order_items = OrderItem.objects.all().order_by("-date_added")[:10]
        items = []
        for x in order_items:
            item = Product.objects.get(id = x.product_id)
            data_dict = {'name':item.name,'image':item.imagesURL,'price':item.price,'id':item.id}
            items.append(data_dict)
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
    s_image = HomepageSlideshow.objects.all()
    
    category = Category.objects.all()
    contex = {'items': items,'order':order,'cartItems':cartItems,'images':s_image,'category':category,'products':items or []}
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
        
        
        
        
        
        
    ms_items = OrderItem.objects.all()
    item_count = []
    item_wise_count = []
    for x in ms_items:
        item = Product.objects.get(id = x.product.id)
        item_count.append(item.id)
    for x in list(dict.fromkeys(item_count)):
        total_order = item_count.count(x)
        data_dict = {x:total_order}
        item_wise_count.append(data_dict)
    print(item_wise_count)
        
        
        
    
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

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def update_item(request):
    if is_ajax(request):
        productId = request.GET.get("productId")
        action = request.GET.get("action")


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
            
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
        
    return JsonResponse({'data': cartItems})


def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        order.total = total

        OrderDetail.objects.create(
            customer=customer,
            order=order,
            mobile=data['form']['mobile'],
            emailaddress=data['form']['email'],
            address=data['form']['address']
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
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
    details = Product.objects.get(pk = id)
    related_product = Product.objects.filter(category = details.category)
    recent_items = OrderItem.objects.filter(category = details.category).values().order_by("-date_added")[:4]
    recents = []
    for item in recent_items:
        product = Product.objects.get(id = item.get("product_id"))
        dict = {"name" : product.name,"image":product.imagesURL}
        recents.append(dict)
    contex = {'details':details,'cartItems':cartItems,'products':related_product,'recents':recents}
    print(contex)
    return render(request,'details.html',contex)

def item_popup_details(request):
    if is_ajax(request):
        product_id = int(request.GET.get("product_id"))
        product = Product.objects.get(id = product_id)
        print(product.imagesURL)
        item = {"id":product.id,'name':product.name,"image":product.imagesURL,"price":product.price,"description":product.descriptions}
    return JsonResponse({'data': item})