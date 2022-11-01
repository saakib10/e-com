from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.sign_in, name='signin'),
    path('login/',views.log_in, name = 'login'),
    path('log_out/',views.log_out, name = 'logout'),
]