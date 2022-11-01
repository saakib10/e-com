from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('shop/', views.shop, name='shop'),
    path('checkout/', views.checkout, name='checkout'),
    path('updateitem/', views.update_item, name='updateitem'),
    path('process_order/',views.processOrder, name = 'processorder'),
    path('details/<int:id>/',views.view_details, name = 'details'),
    path('user/', views.price, name='user')

]
