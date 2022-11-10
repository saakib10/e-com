from django.urls import path

from . import views

urlpatterns = [
        path('user/', views.get_user_order_items, name='user'),
        path('address/', views.set_address_for_customer, name='address_set'),
        path('address/province', views.get_city_data, name="province"),
        path('address/city', views.get_area_data, name="city"),
        path('address/save', views.save_user_address, name="save"),
]