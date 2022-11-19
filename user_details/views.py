from django.shortcuts import render, HttpResponseRedirect
from store.models import *
from django.shortcuts import get_list_or_404, render
from django.http import HttpResponse
from django.shortcuts import get_list_or_404
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
def get_user_order_items(request):
    if request.user.is_authenticated:
        context= {}
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        cartItems = order.get_cart_items
        context['cartItems'] = cartItems
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
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        cartItems = order.get_cart_items
        context['cartItems'] = cartItems
        cmmt = CustomerAddress.objects.filter(customer = customer)
        if cmmt:
            address = CustomerAddress.objects.get(customer = customer)
            details = {}
            if address.province:
                province = {'id': address.province.id,'name': address.province}
                details.update({'province':province})
                pr = Province.objects.filter(~Q(name=address.province))
                context['province'] = pr
            if address.city:
                city = {'id': address.city.id,'name': address.city}
                details.update({'city':city})
                ci = City.objects.filter(~Q(name=address.city))
                context['city'] = ci
            if address.area:
                area = {'id': address.area.id,'name': address.area.name}
                details.update({'area':area})
            if address.address:
                details.update({'address':address.address})
            context['details'] = details
            
        else:
            province = Province.objects.all()
            context['province'] = province
    return render(request,'address_set.html',context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def get_city_data(request):
        if is_ajax(request):
            print("pppp")
            province = request.GET.get("province")
            if not province:
                return
            products = City.objects.filter(province = province).values()
            return JsonResponse({'data': list(products)})
        
        return HttpResponse('Wrong request')
    
def get_area_data(request):
        if is_ajax(request):
            city = request.GET.get("city")
            if not city:
                return
            products = Area.objects.filter(city = city).values()
            return JsonResponse({'data': list(products)})
        
        return HttpResponse('Wrong request')
    
def save_user_address(request):
    if is_ajax(request):
        province = request.GET.get("province")
        city = request.GET.get("city")
        area = request.GET.get("area")
        house = request.GET.get("house")
        print(province)
        customer = request.user.customer
        CustomerAddress.objects.filter(customer=customer).update(province=province  or '',city= city or '',area = area or '',address=house or '')