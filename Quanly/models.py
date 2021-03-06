
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.core.validators import MinValueValidator
#sum

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
    DoSut = models.PositiveIntegerField(default=0, validators= [MinValueValidator(0)])
    Gia = models.PositiveBigIntegerField(validators= [MinValueValidator(0)])
    vatLieu = models.ManyToManyField(VatLieu, through='ChiTietBeTong')
    def __str__(self):
        return self.TenMac


class ChiTietBeTong(models.Model):
    Mac = models.ForeignKey(MacBetong, on_delete= models.CASCADE)
    vatlieu = models.ForeignKey(VatLieu, on_delete=models.CASCADE)
    KhoiLuong = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    class Meta:
        unique_together = [['Mac', 'vatlieu']]


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
    TRANG_THAI = (
        ('R', 'Roi'),
        ('B', 'Ban'),
    )
    trangThaiXe = models.CharField(null=True,max_length=5, choices=TRANG_THAI)
    def __str__(self):
        return self.TenXe + ' '+ self.get_trangThaiXe_display()

class CaLamviec(models.Model):
    CA_LAM = (
        ('S', 'Sang'),
        ('D', 'Dem'),   
    )
    nhanvien = models.ManyToManyField(NhanVien)
    soGio = models.IntegerField()
    caLam = models.CharField(max_length=5, choices=CA_LAM )
    def get_epl_values(self):
        ret = ''
        print(self.nhanvien.all())
        # use models.ManyToMany field's all() method to return all the Department objects that this employee belongs to.
        for dept in self.nhanvien.all():
            ret = ret + dept.HoTen + ', '
        # remove the last ',' and return the value.
        return ret[:-2]

class TramTron(models.Model):
    tenTramTron = models.CharField(max_length=30)
    dungTich = models.CharField(max_length=10)
    def __str__(self):
        return self.tenTramTron
# phan quyen nhan vien tram tron
class NhanVienQlyTramTron(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(trangThai = 'dgh')

class NhanVienQlyDh(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(trangThai = 'xl')


class Donhang(models.Model):
    TRANG_THAI = (
        ('cxl', 'Chua xu li'),
        ('xl', 'da xu li'), 
        ('dgh', 'da giao hang'), 
    )
    khachHang = models.ForeignKey(KhachHang, on_delete= models.CASCADE)
    tramTron = models.ForeignKey(TramTron,on_delete= models.CASCADE)
    mac = models.ForeignKey(MacBetong, on_delete= models.CASCADE)
    soKhoi = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    tongGia = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0)]) #soKhoi * MacBetong.Gia
    ngayTao = models.DateTimeField(auto_now_add=True)
    ngayDo = models.DateTimeField()
    trangThai = models.CharField(max_length=30, choices=TRANG_THAI )
    Xe = models.ManyToManyField(XeBon, through='ChiTietDonHang')
    object = models.Manager()
    nvBanhang = NhanVienQlyDh()
    QLTramTron = NhanVienQlyTramTron()
    def __str__(self):
        return 'DON HANG '+ str(self.id)
    @property
    def diff_d_count(self):
        dt=0
        for dtt in Donhang.object.filter(trangThai = 'dgh'):
            dt = dt + dtt.soKhoi *  dtt.mac.Gia
        return dt
    def Total(self):
        return self.soKhoi * self.mac.Gia
    
# class QuanLyDonHang (models.Model):
#     donHang = models.ForeignKey(Donhang, on_delete=models.CASCADE) 
#     nhanVien = models.ForeignKey(NhanVien)
class ChiTietDonHang (models.Model):
    donHang = models.ForeignKey(Donhang, on_delete=models.CASCADE) 
    xeBon = models.ForeignKey(XeBon,on_delete=models.CASCADE)
    class Meta:
        unique_together = [['donHang', 'xeBon']]

