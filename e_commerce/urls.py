from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('store.urls')),
    path('about/',include('about.urls')),
    path('auth/',include('authentication.urls')),
    path('user/',include('user_details.urls')),
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
