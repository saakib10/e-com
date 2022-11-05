from django.urls import path

from . import views

urlpatterns = [
        path('user/', views.get_user_order_items, name='user'),
        path('address/', views.set_address_for_customer, name='address_set')
]