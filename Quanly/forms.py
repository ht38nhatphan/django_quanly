
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.template.defaulttags import widthratio
from django import forms
import datetime
from .models import Donhang, KhachHang
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class AddCustomer(forms.ModelForm):
     class Meta:
        model =  KhachHang
        fields = ['HoTen', 'SoDienThoai', 'DiaChi', 'SoCMT']

# create user
class UserAddForm(UserCreationForm):
	'''
	Extending UserCreationForm - with email

	'''
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'eg.edwards@rabotecgroup.com'}))

	class Meta:
		model = User
		fields = ['username','email','password1','password2']
		

	def clean_email(self):
		email = self.cleaned_data['email']
		qry = User.objects.filter(email = email)

		domain_list = ['rabotecgroup.com','rabotecghana.com']
		get_rabotec_domain = email.split('@')[1]#get me whatever after @, eg. gmail.com

		print(get_rabotec_domain in domain_list)

		if qry.exists():
			'''
			True - Queryset exist run validation message here
			'''
			raise forms.ValidationError('email {0} already exists'.format(email))


		elif get_rabotec_domain not in domain_list:
			print('test - not in domain')
			raise forms.ValidationError('email does not contain domain')

		return email
# login
class UserLogin(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))


# order

class AddOrder(forms.ModelForm):
	ngayDo = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])
	ngayTao = forms.DateTimeField( required=True, input_formats=["%Y-%m-%dT%H:%M", ])
	class Meta:
		model = Donhang	
		fields = ['khachHang', 'tramTron', 'mac', 'soKhoi','ngayDo' ,'tongGia' , 'trangThai' ]
		# fields = '__all__'
        # widgets = {
        #     'my_date': DateInput(attrs={'type': 'date'})
        # }
