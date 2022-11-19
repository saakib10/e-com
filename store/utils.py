from .models import *
from .views import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def set_order_details_with_address(request):
    if request.user.is_authenticated:
        if is_ajax(request):
            user_address = int(request.GET.get("user_address"))
            customer = request.user.customer
            if user_address == 1:
                address = get_customer_address(customer)
                order, created = Order.objects.get_or_create(customer=customer, complete=False)
                OrderDetail.objects.create(
                    customer=customer,
                    order=order,
                    province=address.province,
                    city=address.city,
                    area = address.area,
                    address=address.address
                )
                
        return HttpResponse('Request Prosessing')
            
            
            
# Get Customer Address For 
def get_customer_address(customer):
    address = CustomerAddress.objects.filter(customer = customer).exists()
    if address:
        addr = CustomerAddress.objects.get(customer = customer)
        return {
            'province':addr.province,
            'city':addr.city,
            'area':addr.area,
            'address':addr.address
        }