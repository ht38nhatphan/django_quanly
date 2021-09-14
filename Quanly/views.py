
from django.db.models.aggregates import Count, Min
from django.http.response import HttpResponse
from django.contrib.auth.models import Group 
from django.shortcuts  import render, redirect,get_list_or_404,get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DeleteView
from .forms import AddCustomer, AddShift, AddStaff,UserLogin,UserAddForm,AddOrder
from django.contrib import messages
from django.contrib.auth.models import Group,User,UserManager

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
	data = { 'khachhang': KhachHang.objects.all() }
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
        dataset['title'] = 'create customer'
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
	query = "SELECT A.id, C.HoTen as tkh, B.TenMac, soKhoi,B.Gia, soKhoi * B.Gia as tong , ngayTao, ngayDo, trangThai FROM Quanly_donhang A join Quanly_macbetong B on A.mac_id = B.id  JOIN Quanly_khachhang C on A.khachHang_id = C.id join Quanly_tramtron E on A.tramTron_id = E.id WHERE trangThai = 'cxl';"
	query1 = "SELECT A.id, C.HoTen as tkh, B.TenMac, soKhoi,B.Gia, soKhoi * B.Gia as tong , ngayTao, ngayDo, trangThai FROM Quanly_donhang A join Quanly_macbetong B on A.mac_id = B.id  JOIN Quanly_khachhang C on A.khachHang_id = C.id join Quanly_tramtron E on A.tramTron_id = E.id WHERE trangThai = 'xl' or trangThai='dgh' ;"
	data = {'donhang': Donhang.object.raw(query),
		'donhang1': Donhang.object.raw(query),
	}
	# data = { 'donhang1': Donhang.QLTramTron.all(), 
	# 		'donhang2': Donhang.nvBanhang.all()  }
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
		if request.method == 'POST':
			form = AddOrder(data = request.POST or None)
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
				instance.tongGia = request.POST.get('tongGia')
				
				# instance.ngayTao = request.POST.get('ngayTao')
				# instance.ngayDo = request.POST.get('ngayDo')
				
				instance.trangThai = request.POST.get('trangThai')
				#check status in tt 
				group = Group.objects.get(name = "Quản lý trạm trộn")
				check = True if group in request.user.groups.all() else False
				if request.POST.get('trangThai') == 'xl' and not check:
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
		form = AddOrder()
		dataset['form'] = form
		dataset['title'] = 'TAO DON HANG'
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


# ---------------------------------nv ------------------------
def staff(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	data = { 'nhanvien': NhanVien.objects.all() }
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
		dataset['title'] = 'create Staff'
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
				return redirect('Quanly:addstaff')
			else:
				messages.error(request,'Error Staff ',extra_tags = 'alert alert-warning alert-dismissible show')
				return redirect('Quanly:addstaff')

		dataset = dict()
		form = AddStaff(request.POST or None,instance = staff)
		dataset['form'] = form
		dataset['title'] = 'edit Staff'
		return render(request,'staff/addStaff.html',dataset)	
def delete_staff(request,id):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	else:
		get_object_or_404(NhanVien, id = id).delete()
		return redirect('Quanly:staff')



#  Quan ly xe

def Car(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	data = { 'Xe': XeBon.objects.all() }
	return render(request, 'Car/car.html', data)


# Quan ly ca truc

def Shift(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	data = { 'Ca': CaLamviec.objects.all() }
	return render(request, 'Shift/shift.html', data)

def Add_shift(request):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	else:
		if request.method == 'POST':
			form = AddShift(data = request.POST)
			if form.is_valid():
			
				form.save()

				messages.success(request,'Shift Successfully Created ',extra_tags = 'alert alert-success alert-dismissible show')
				return redirect('Quanly:addshift')
			else:
				messages.error(request,'Error Creating Shift ',extra_tags = 'alert alert-warning alert-dismissible show')
				return redirect('Quanly:addshift')

		dataset = dict()
		form = AddShift()
		dataset['form'] = form
		dataset['title'] = 'create Shift'
		return render(request,'Shift/addShift.html',dataset)

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
