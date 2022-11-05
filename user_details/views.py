from django.shortcuts import render, HttpResponseRedirect
from store.models import *

# Create your views here.
def get_user_order_items(request):
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
                    data_dict["amount"] = x.get('total')
                    items.append(data_dict)
            context["items"] = items
        # get user details
        details = {}
        details['email'] = customer.email
        details['mobile'] = customer.mobile
        context['details'] = details
    return render(request,'user_order_details.html',context)


def set_address_for_customer(request):
    if request.user.is_authenticated:
        context = {}
        customer = request.user.customer
        cmmt = CustomerAddress.objects.filter(customer = customer)
        if cmmt:
            address = CustomerAddress.objects.get(customer = customer)
            details = {}
            details['province'] = address.province
            details['city'] = address.city
            details['area'] = address.area
            details['address'] = address.address
            context['details'] = details
        
    return render(request,'address_set.html',context)