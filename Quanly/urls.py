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
    path('qlkh/view_order_detail/<int:id>', views.view_Order_detail,name='view_order_detail'),
    
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
    # -------------------- material --------------------------------------------
    path('Matirial/', views.Material,name='Material'),
    path('add_material/', views.add_material,name='add_material'),
    path('Matirial/edit_material/<int:id>', views.edit_material,name='edit_material'),
    path('Matirial/delete_material/<int:id>',views.delete_material,name='delete_material'),
    #------------------------Concrete --------------------------------------------------------
    path('Concrete/', views.Concrete,name='Concrete'),
    path('add_concrete/', views.add_concrete,name='add_concrete'),
    path('Concrete/view_concret_detail/<int:id>', views.view_concrete_detail,name='view_concrete_detail'),
    path('Concrete/edit_concrete/<int:id>', views.edit_concrete,name='edit_concrete'),
    path('Concrete/delete_concrete/<int:id>',views.delete_concrete,name='delete_concrete'),
    #--------------------------Station----------------------------------------------
    path('Station/', views.Station,name='Station'),
    path('add_station/', views.add_station,name='add_station'),
    path('Station/edit_Station/<int:id>', views.edit_station,name='edit_station'),
    path('Station/delete_station/<int:id>',views.delete_station,name='delete_station'),
    #--------------------------Concrete_detail----------------------------------------------
    path('Concrete_detail/', views.Concrete_detail,name='Concrete_detail'),
    path('add_concrete_detail/', views.add_concrete_detail,name='add_concrete_detail'),
    path('Concrete_detail/edit_concrete_detail/<int:id>', views.edit_concrete_detail,name='edit_concrete_detail'),
    path('Concrete_detail/delete_concrete_detail/<int:id>',views.delete_concrete_detail,name='delete_concrete_detail'),
]
