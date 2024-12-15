from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='home'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('login/', views.custom_login, name='login'),  # Use built-in LoginView if desired
    path('map/', views.maps, name='map'),  # Use built-in LoginView if desired
    path('logout/', views.logout_view, name='logout'),
    path('api/send-coordinates/', views.send_coordinates, name='send_coordinates'),

]
