from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('shop/', views.shop, name='shop'),
    path('checkout/', views.checkout, name='checkout'),
    path('updateitem/', views.update_item, name='updateitem'),
    path('sign_in/',views.sign_in, name = 'signin'),
    path('log_in/',views.log_in, name = 'login'),
    path('process_order/',views.processOrder, name = 'processorder'),
    path('log_out/',views.log_out, name = 'logout'),
    path('details/<int:id>/',views.view_details, name = 'details'),

]
