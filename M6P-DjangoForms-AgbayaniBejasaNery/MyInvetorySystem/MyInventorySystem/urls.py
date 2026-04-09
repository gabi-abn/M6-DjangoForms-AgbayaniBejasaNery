from django.contrib import admin
from django.urls import path
from MyInventoryApp import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('view_supplier/', views.view_supplier, name='view_supplier'),
    path('view_bottles/<int:supplier_id>/', views.view_bottles, name='view_bottles'),
    path('view_bottle_details/<int:pk>/', views.view_bottle_details, name='view_bottle_details'),
    path('add_bottle/', views.add_bottle, name='add_bottle'),
    path('signup/', views.signup_view, name='signup'),
]
