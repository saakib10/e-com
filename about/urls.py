from django.urls import path

from . import views

urlpatterns = [
        path('page/',views.about_us,name = 'about'),
]