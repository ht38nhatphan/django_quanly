from django.contrib import admin
from .models import XeBon,NhanVien,CaLamviec,ChiTietBeTong,CongViec,KhachHang,MacBetong,VatLieu,Donhang,TramTron
# Register your models here.
admin.site.register(KhachHang)
admin.site.register(VatLieu)
admin.site.register(XeBon)
admin.site.register(NhanVien)
admin.site.register(CaLamviec)
admin.site.register(ChiTietBeTong)
admin.site.register(CongViec)
admin.site.register(MacBetong)
admin.site.register(Donhang)
admin.site.register(TramTron)
