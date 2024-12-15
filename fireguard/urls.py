from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('maps.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Add this for authentication views

]
