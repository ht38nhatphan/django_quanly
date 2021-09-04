from django.db import models
from django.db.models.fields.related import ForeignKey
#sum
from django.db.models import F

class AnnotationManager(models.Manager):

    def __init__(self, **kwargs):
        super().__init__()
        self.annotations = kwargs

    def get_queryset(self):
        return super().get_queryset().annotate(**self.annotations)
# Create your models here.
class KhachHang(models.Model):
     HoTen = models.TextField(max_length=40)
     SoDienThoai = models.CharField(max_length=10)
     DiaChi = models.TextField(max_length=100)
     SoCMT = models.TextField(max_length=20)
     def __str__(self):
        return self.HoTen + ' ' + self.SoDienThoai
class VatLieu(models.Model):
    TenVatLieu = models.TextField(max_length=50)
    DonVi = models.TextField(max_length=10)
    def __str__(self):
        return self.TenVatLieu

class MacBetong(models.Model):
    TenMac = models.TextField(max_length=30)
    DoSut = models.TextField(max_length=20)
    Gia = models.BigIntegerField()
    vatLieu = models.ManyToManyField(VatLieu, through='ChiTietBeTong')
    def __str__(self):
        return self.TenMac

class ChiTietBeTong(models.Model):
    Mac = models.ForeignKey(MacBetong, on_delete= models.CASCADE)
    vatlieu = models.ForeignKey(VatLieu, on_delete=models.CASCADE)
    KhoiLuong = models.IntegerField()

class CongViec(models.Model):
    TenCongViec = models.TextField(max_length=50)
    def __str__(self):
        return self.TenCongViec

class NhanVien(models.Model):
    HoTen = models.TextField(max_length=40)
    congViec= models.ForeignKey(CongViec, on_delete= models.CASCADE)
    SoDienThoai = models.CharField(max_length=10)
    DiaChi = models.TextField(max_length=100)
    SoCMT = models.TextField(max_length=20)
    def __str__(self) :
        return self.HoTen + ' ' + self.congViec.TenCongViec

class XeBon(models.Model):
    TenXe = models.TextField(max_length=40)
    BienSo = models.TextField(max_length=20)
    nhanVien = models.ForeignKey(NhanVien, on_delete= models.CASCADE)

class CaLamviec(models.Model):
    CA_LAM = (
        ('S', 'Sang'),
        ('D', 'Dem'),   
    )
    nhanvien = models.ManyToManyField(NhanVien)
    soGio = models.IntegerField()
    caLam = models.CharField(max_length=5, choices=CA_LAM )

class TramTron(models.Model):
    tenTramTron = models.CharField(max_length=30)
    dungTich = models.CharField(max_length=10)
    def __str__(self):
        return self.tenTramTron
# phan quyen nhan vien tram tron
class NhanVienQlyTramTron(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(trangThai = 'xl') and super().get_queryset().filter(trangThai = 'dgh')

class NhanVienQlyDh(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(trangThai = 'cxl') 

class Donhang(models.Model):
    TRANG_THAI = (
        ('cxl', 'Chua xu li'),
        ('xl', 'da xu li'), 
        ('dgh', 'da giao hang'), 
    )
    khachHang = models.ForeignKey(KhachHang, on_delete= models.CASCADE)
    tramTron = models.ForeignKey(TramTron,on_delete= models.CASCADE)
    mac = models.ForeignKey(MacBetong, on_delete= models.CASCADE)
    soKhoi = models.IntegerField()
    _tongGia = None #soKhoi * MacBetong.Gia
    ngayTao = models.TimeField(auto_now_add=True)
    ngayDo = models.TimeField()
    trangThai = models.CharField(max_length=30, choices=TRANG_THAI )
    nvBanhang = NhanVienQlyDh()
    QLTramTron = NhanVienQlyTramTron()
    objects = AnnotationManager(
        tongGia = F('soKhoi') * F('soKhoi')
    )

# class QuanLyDonHang (models.Model):
#     donHang = models.ForeignKey(Donhang, on_delete=models.CASCADE) 
#     nhanVien = models.ForeignKey(NhanVien)