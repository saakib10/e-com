from django.shortcuts import render
from store.models import *
# Create your views here.

def about_us(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete = False)
        cartItems = order.get_cart_items

    else:
        cartItems = 0

    contex = {'cartItems':cartItems}
    return render(request,'about.html',contex)