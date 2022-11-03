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
                    items.append(data_dict)
            context["items"] = items
    return render(request,'user_order_details.html',context)