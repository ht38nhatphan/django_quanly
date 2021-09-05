from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'Quanly'
urlpatterns = [
    path('',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('home/', views.index, name='index'),   
    path('qlnv/', views.staff, name='staff'), 
    path('qlkh/', views.customer, name='customer'), 
    path('addkh/', views.addcustomer, name='addcustomer'), 
    path('od/', views.order, name='order'),
    path('qlkh/<int:id>/', views.editcustomer, name='edit_customer'), 
    path('qlkh/de/<int:id>/', views.deletecustomer, name='delete_customer'),
    path('order/',views.add_oder,name='add_order'),
#     path('savekh/', views.saveCustomer, name='savecustomer'),
#    order
    

]
