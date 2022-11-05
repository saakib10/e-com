from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderDetail)
admin.site.register(Category)
admin.site.register(HomepageSlideshow)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(CustomerAddress)