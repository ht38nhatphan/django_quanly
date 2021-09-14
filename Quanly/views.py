
from django.db.models.aggregates import Count, Min
from django.http.response import HttpResponse
from django.contrib.auth.models import Group 
from django.shortcuts  import render, redirect,get_list_or_404,get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DeleteView
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import Group,User,UserManager
import datetime
from django.db.models import F
from django.db import connection
from django.utils.dateparse import parse_date
# Create your views here.
#------------------------------------MAIN---------------------------
def index(request):
    if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
        return redirect('/')

    return render(request, 'index.html')

#---------------------------------------CUSTOMER-----------------------
def customer(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	data = { 'khachhang': KhachHang.objects.all(),'title' : 'QUAN LY KHACH HANG'}
	return render(request, 'customer.html', data)

def addcustomer(request):
    if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
        return redirect('/')
    else:
        if request.method == 'POST':
            form = AddCustomer(data = request.POST)
            if form.is_valid():
                instance = form.save(commit = False)

                instance.HoTen= request.POST.get('HoTen')
                instance.SoDienThoai = request.POST.get('SoDienThoai')
                instance.DiaChi = request.POST.get('DiaChi')
                instance.SoCMT = request.POST.get('SoCMT')

                instance.save()


                messages.success(request,'customer Successfully Created ',extra_tags = 'alert alert-success alert-dismissible show')
                return redirect('Quanly:addcustomer')

            else:
                messages.error(request,'Error Creating Customer ',extra_tags = 'alert alert-warning alert-dismissible show')
                return redirect('Quanly:addcustomer')

        dataset = dict()
        form = AddCustomer()
        dataset['form'] = form
        dataset['title'] = 'TAO KHACH HANG'
        return render(request,'addCustomer.html',dataset)

def editcustomer(request,id):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	customer = get_object_or_404(KhachHang, id = id)
	if request.method == 'POST':
		form = AddCustomer(data = request.POST,instance = customer)
		if form.is_valid():
			instance = form.save(commit = False)
			instance.HoTen= request.POST.get('HoTen')
			instance.SoDienThoai = request.POST.get('SoDienThoai')
			instance.DiaChi = request.POST.get('DiaChi')
			instance.SoCMT = request.POST.get('SoCMT')
			instance.save()
			
			messages.success(request,'Customer Successfully  ',extra_tags = 'alert alert-success alert-dismissible show')
			return redirect('Quanly:addcustomer')
		else:
			messages.error(request,'Error Creating Customer ',extra_tags = 'alert alert-warning alert-dismissible show')
			return redirect('Quanly:addcustomer')
		
	dataset = dict()
	form = AddCustomer(request.POST or None,instance = customer)
	dataset['form'] = form
	dataset['title'] = 'EDIT CUSTOMER'
	return render(request,'addCustomer.html',dataset)

def deletecustomer(request,id):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	else:
		get_object_or_404(KhachHang, id = id).delete()
		return redirect('Quanly:customer')

		

# SELECT soKhoi,B.Gia, soKhoi * B.Gia as tong ,tongGia, ngayTao, ngayDo, trangThai, khachHang_id, mac_id, tramTron_id
# FROM Quanly_donhang A join Quanly_macbetong B on A.mac_id = B.id WHERE trangThai = 'xl';
#------------------------------------------------ORDER-----------------------------------------
def order(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	# query = "SELECT A.id, C.HoTen as tkh, B.TenMac, soKhoi,B.Gia, soKhoi * B.Gia as tong , ngayTao, ngayDo, trangThai FROM Quanly_donhang A join Quanly_macbetong B on A.mac_id = B.id  JOIN Quanly_khachhang C on A.khachHang_id = C.id join Quanly_tramtron E on A.tramTron_id = E.id WHERE trangThai = 'cxl';"
	# query1 = "SELECT A.id, C.HoTen as tkh, B.TenMac, soKhoi,B.Gia, soKhoi * B.Gia as tong , ngayTao, ngayDo, trangThai FROM Quanly_donhang A join Quanly_macbetong B on A.mac_id = B.id  JOIN Quanly_khachhang C on A.khachHang_id = C.id join Quanly_tramtron E on A.tramTron_id = E.id  ;"
	# data = {'donhang': Donhang.object.raw(query),
	# 	'donhang1': Donhang.object.raw(query1),
	# 	'donhangall': Donhang.object.all(),
	# 	'title': 'THONG TIN DON HANG'
	# }
	data = { 'donhang1': Donhang.QLTramTron.all(), 
			'donhang2': Donhang.nvBanhang.all()  ,
			'donhang': Donhang.object.all()}
	return render(request, 'Order/order.html', data)
def delete_order(request,id):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	else:
		get_object_or_404(Donhang, id = id).delete()
		return redirect('Quanly:order')
def add_oder(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	else:
		group = Group.objects.get(name = "Quản lý trạm trộn")
		check = True if group in request.user.groups.all() else False
		group1 = Group.objects.get(name = "Bán hàng")
		check1 = True if group1 in request.user.groups.all() else False

		if request.method == 'POST':
			form = AddOrderdh(data = request.POST) if check1 == True else AddOrdertt(data = request.POST) if check==True else AddOrder(data = request.POST)
			
			if form.is_valid():
				
				instance = form.save(commit = False)
				idcustomer = request.POST.get('khachHang')
				idtram = request.POST.get('tramTron')
				idmac = request.POST.get('mac')
				tramobj = get_object_or_404(TramTron,id = idtram)
				cusobj = get_object_or_404(KhachHang,id = idcustomer)
				macobj = get_object_or_404(MacBetong,id = idmac)
				instance.khachHang = cusobj
				instance.tramTron = tramobj
				instance.mac = macobj
				instance.soKhoi = request.POST.get('soKhoi')
				
				
				# instance.ngayTao = request.POST.get('ngayTao')
				# instance.ngayDo = None
				
				instance.trangThai = request.POST.get('trangThai')
				#check status in tt 
				if request.POST.get('trangThai') == 'xl' and not check or request.POST.get('trangThai') == 'dgh' and not check:
					messages.error(request,'Error Creating Customer ',extra_tags = 'alert alert-warning alert-dismissible show')
					return redirect('Quanly:add_order')
				else:
					instance.save()
				messages.success(request,'order Successfully Created ',extra_tags = 'alert alert-success alert-dismissible show')
				return redirect('Quanly:add_order')

			else:
				messages.error(request,'Error Creating Customer ',extra_tags = 'alert alert-warning alert-dismissible show')
				return redirect('Quanly:add_order')

		dataset = dict()
		form = AddOrderdh() if check1 == True else AddOrdertt() if check==True else AddOrder()
		dataset['form'] = form
		dataset['title'] = 'TAO DON HANG'
		return render(request,'Order/addOrder.html',dataset)
def edit_order(request,id):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	else:
		order = get_object_or_404(Donhang,id=id)
		group = Group.objects.get(name = "Quản lý trạm trộn")
		check = True if group in request.user.groups.all() else False
		group1 = Group.objects.get(name = "Bán hàng")
		check1 = True if group1 in request.user.groups.all() else False

		if request.method == 'POST':
			form = AddOrderdh(data = request.POST,instance = order) if check1 == True else AddOrdertt(data = request.POST,instance = order) if check==True else AddOrder(data = request.POST,instance = order)
			if form.is_valid():
				instance = form.save(commit = False)
				if not check:
					idcustomer = request.POST.get('khachHang')
					idtram = request.POST.get('tramTron')
					idmac = request.POST.get('mac')
					tramobj = get_object_or_404(TramTron,id = idtram)
					cusobj = get_object_or_404(KhachHang,id = idcustomer)
					macobj = get_object_or_404(MacBetong,id = idmac)
					instance.khachHang = cusobj
					instance.tramTron = tramobj
					instance.mac = macobj
					instance.soKhoi = request.POST.get('soKhoi')
				instance.trangThai = request.POST.get('trangThai')
				#check status in tt 
				# la qun ly ban hang thi cho sua ngay tao
				# if request.POST.get('trangThai') == 'xl' and not check or request.POST.get('trangThai') == 'dgh' and not check:
				# 	instance.ngayDo = request.POST.get('ngayDo')
				# 	instance.save()
				# 	return redirect('Quanly:order')
				# la qun ly tram tron thi cho sua ngay do
				if check:
					instance.save()
					return redirect('Quanly:order')
				else:
					instance.save()
					return redirect('Quanly:order')

			else:
				messages.error(request,'Error Creating Customer ',extra_tags = 'alert alert-warning alert-dismissible show')
				return redirect('Quanly:add_order')

		dataset = dict()
		form = AddOrderdh(request.POST or None,instance = order) if check1 == True else AddOrdertt(request.POST or None,instance = order) if check==True else AddOrder(request.POST or None,instance = order)
		dataset['form'] = form
		dataset['title'] = 'CHINH SUA DON HANG'
		return render(request,'Order/addOrder.html',dataset)
#------------------------------------------------account-----------------------------------------

# login
def login_view(request):
	'''
	work on me - needs messages and redirects
	
	'''
	login_user = request.user
	if request.method == 'POST':
		form = UserLogin(data = request.POST)
		if form.is_valid():
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username = username, password = password)
			if user and user.is_active:
				login(request,user)
				if login_user.is_authenticated:
					return redirect('Quanly:index')
			else:
			    messages.error(request,'Account is invalid',extra_tags = 'alert alert-error alert-dismissible show' )
			    return redirect('Quanly:login')

		else:
			return HttpResponse('data not valid')

	dataset=dict()
	form = UserLogin()
	dataset['form'] = form
    
	return render(request,'accounts/login.html',dataset)

# logout
def logout_view(request):
	logout(request)
	return redirect('Quanly:login')


# --------------------------------- NV ------------------------
def staff(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	data = { 'nhanvien': NhanVien.objects.all(),'title' : 'THONG TIN NHAN VIEN' }
	
	return render(request, 'staff/staff.html', data)

def add_staff(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	else:
		if request.method == 'POST':
			form = AddStaff(data = request.POST)
			if form.is_valid():
				instance = form.save(commit = False)

				instance.HoTen= request.POST.get('HoTen')
				idcv = request.POST.get('congViec')
				cvobj = get_object_or_404(CongViec,id = idcv)
				instance.congViec = cvobj
				instance.SoDienThoai = request.POST.get('SoDienThoai')
				instance.DiaChi = request.POST.get('DiaChi')
				instance.SoCMT = request.POST.get('SoCMT')
				instance.save()


				messages.success(request,'Staff Successfully Created ',extra_tags = 'alert alert-success alert-dismissible show')
				return redirect('Quanly:addstaff')
			else:
				messages.error(request,'Error Creating Staff ',extra_tags = 'alert alert-warning alert-dismissible show')
				return redirect('Quanly:addstaff')

		dataset = dict()
		form = AddStaff()
		dataset['form'] = form
		dataset['title'] = 'TAO NHAN VIEN'
		return render(request,'staff/addStaff.html',dataset)
def edit_staff(request,id):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	
	else:
		staff = get_object_or_404(NhanVien,id=id)
		if request.method == 'POST':
			form = AddStaff(data = request.POST,instance = staff)
			if form.is_valid():
				instance = form.save(commit = False)

				instance.HoTen= request.POST.get('HoTen')
				idcv = request.POST.get('congViec')
				cvobj = get_object_or_404(CongViec,id = idcv)
				instance.congViec = cvobj
				instance.SoDienThoai = request.POST.get('SoDienThoai')
				instance.DiaChi = request.POST.get('DiaChi')
				instance.SoCMT = request.POST.get('SoCMT')
				instance.save()


				messages.success(request,'Staff Successfully ',extra_tags = 'alert alert-success alert-dismissible show')
				
			else:
				messages.error(request,'Error Staff ',extra_tags = 'alert alert-warning alert-dismissible show')
				return redirect('Quanly:addstaff')

		dataset = dict()
		form = AddStaff(request.POST or None,instance = staff)
		dataset['form'] = form
		dataset['title'] = 'SUA THONG TIN NHAN VIEN'
		return render(request,'staff/addStaff.html',dataset)	
def delete_staff(request,id):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	else:
		get_object_or_404(NhanVien, id = id).delete()
		return redirect('Quanly:staff')

# ---------------------------- quan ly Car -------------------------------------

def Car(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	data = { 'Xe': XeBon.objects.all(), 'title': 'QUAN LY XE' }
	return render(request, 'Car/car.html', data)

def add_car(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	else:
		if request.method == 'POST':
			form = AddCar(request.POST or None)
			if form.is_valid():
				form.save()
				messages.success(request,'Car Successfully Created ',extra_tags = 'alert alert-success alert-dismissible show')
				return redirect('Quanly:AddCar')
			else:
				messages.error(request,'Error Creating Car ',extra_tags = 'alert alert-warning alert-dismissible show')
				return redirect('Quanly:AddCar')

		dataset = dict()
		form = AddCar()
		dataset['form'] = form
		dataset['title'] = 'NHAP XE BON'
		return render(request,'Car/add_car.html',dataset)				
def edit_car(request, id):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')	
	else:
		car = get_object_or_404(XeBon,id=id)
		if request.method == 'POST':
			form = AddCar(data = request.POST,instance = car)
			if form.is_valid():
				form.save()
				messages.success(request,'Car Successfully Edit ',extra_tags = 'alert alert-success alert-dismissible show')
				# return 1
			else:
				messages.error(request,'Error Creating Car ',extra_tags = 'alert alert-warning alert-dismissible show')
				return redirect('Quanly:edit_car')

		dataset = dict()
		form = AddCar(request.POST or None,instance = car)
		dataset['form'] = form
		dataset['title'] = 'SUA THONG TIN XE'
		return render(request,'Car/add_car.html',dataset)

def delete_car(request,id):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	else:
		get_object_or_404(XeBon, id = id).delete()
		return redirect('Quanly:Car')	
# ------------------------------Quan ly ca truc-------------------------------

def Shift(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	data = { 'Ca': CaLamviec.objects.all(),'title' :'QUAN LY CA TRUC' }
	return render(request, 'Shift/shift.html', data)

#add shift
def add_shift(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	else:
		if request.method == 'POST':
			form = AddShift(request.POST or None)
			if form.is_valid():
				instance = form.save(commit=False)
				idnv = request.POST.getlist('nhanvien')
				# print(idnv)
				for i in idnv:
					nvobj = get_object_or_404(NhanVien,id = i)
					# print(nvobj)
					instance.save()
					instance.nhanvien.add(nvobj)
				instance.soGio = request.POST.get('soGio')
				instance.caLam = request.POST.get('caLam')
				instance.save()
				messages.success(request,'Shift Successfully Created ',extra_tags = 'alert alert-success alert-dismissible show')
				return redirect('Quanly:Addshift')
			else:
				messages.error(request,'Error Creating Shift ',extra_tags = 'alert alert-warning alert-dismissible show')
				return redirect('Quanly:Addshift')

		dataset = dict()
		form = AddShift()
		dataset['form'] = form
		dataset['title'] = 'THEM CA LAM'
		return render(request,'Shift/add_shift.html',dataset)

# daskboard
def Daskboard(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	
	data = {'Cus': KhachHang.objects.count(), #dem so khach hang
			'Dh': Donhang.object.count(), # dem so don hang
			'doanhthu': Donhang.object.filter(trangThai = 'dgh')[:1],
			'donhang': Donhang.object.all(),
			'dhcxl': Donhang.object.exclude(trangThai = 'dgh' ).count()
			# 'doanhthu' : Donhang.object.raw(query)
	 }
	print(data['doanhthu'])
	return render(request, 'index2.html', data)
					
def edit_shift(request, id):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')	
	else:
		shift = get_object_or_404(CaLamviec,id= id)
		if request.method == 'POST':
			form = AddShift(data = request.POST,instance = shift)
			if form.is_valid():
				instance = form.save(commit=False)
				idnv = request.POST.getlist('nhanvien')
				instance.nhanvien.clear()
				for i in idnv:
					nvobj = get_object_or_404(NhanVien,id = i)
					print(nvobj)
					instance.save()
					instance.nhanvien.add(nvobj)
				instance.soGio = request.POST.get('soGio')
				instance.caLam = request.POST.get('caLam')
				instance.save()
				messages.success(request,'Shift Successfully Edit ',extra_tags = 'alert alert-success alert-dismissible show')
				# return 1
			else:
				messages.error(request,'Error Creating Shift ',extra_tags = 'alert alert-warning alert-dismissible show')
				return redirect('Quanly:edit_shift')

		dataset = dict()
		form = AddShift(request.POST or None,instance = shift)
		dataset['form'] = form
		dataset['title'] = 'SUA CA LAM VIEC'
		return render(request,'Shift/add_shift.html',dataset)

def delete_shift(request,id):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	else:
		get_object_or_404(CaLamviec, id = id).delete()
		return redirect('Quanly:Shift')
