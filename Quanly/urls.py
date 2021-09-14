from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'Quanly'
urlpatterns = [
    path('',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('home/', views.index, name='index'),   
    path('qlnv/', views.staff, name='staff'),
    path('addstaff/',views.add_staff,name='addstaff'),
    path('qlnv/editsaff/<int:id>/',views.edit_staff,name='editstaff'),
    path('qlnv/delstaff/<int:id>/',views.delete_staff,name='delstaff'),
    path('qlkh/', views.customer, name='customer'), 
    path('addkh/', views.addcustomer, name='addcustomer'), 
    path('od/', views.order, name='order'),
    path('qlkh/<int:id>/', views.editcustomer, name='edit_customer'), 
    path('qlkh/de/<int:id>/', views.deletecustomer, name='delete_customer'),
    path('order/',views.add_oder,name='add_order'),
    path('order/edit_order/<int:id>/', views.edit_order, name='edit_order'),
    path('qlkh/delete_order/<int:id>/', views.delete_order, name='delete_order'),
    
    path('Shift/',views.Shift,name='Shift'),

    path('Addshift/',views.add_shift,name='Addshift'),
    path('Shift/edit/<int:id>',views.edit_shift,name='edit_shift'),
    path('Shift/delete/<int:id>',views.delete_shift, name='delete_shift'),

    path('Car/',views.Car,name='Car'),
    path('AddCar/',views.add_car,name='AddCar'),
    path('Car/edit/<int:id>',views.edit_car,name='edit_car'),
    path('Car/delete/<int:id>',views.delete_car, name='delete_car'),
     path('daskboard/', views.Daskboard, name = 'dask'),
#     path('savekh/', views.saveCustomer, name='savecustomer'),
#    order
    

]
