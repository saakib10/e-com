from django.contrib import admin

from .models import *

admin.site.register(Customer)
class MyProduct(admin.ModelAdmin):
    list_display = ('name', 'category',)
    list_filter = (
        ('category', admin.RelatedOnlyFieldListFilter),
    )
admin.site.register(Product, MyProduct)


admin.site.register(Order)
admin.site.register(OrderItem)


class MyOrderDetails(admin.ModelAdmin):
    list_display = ('customer',)
    list_filter = (
        ('customer', admin.RelatedOnlyFieldListFilter),
    )
admin.site.register(OrderDetail,MyOrderDetails)

admin.site.register(Category)
admin.site.register(HomepageSlideshow)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(CustomerAddress)