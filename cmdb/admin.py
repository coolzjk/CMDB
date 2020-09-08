from django.contrib import admin
# from django.contrib.auth import *  #加这句出问题
from cmdb.models import *
from django.contrib.auth import models

class idccontrol(admin.ModelAdmin):
    list_display = ('name','floor','address','RackNum')
class usercontrol(admin.ModelAdmin):
    list_display = ('id','name','codename')
class permission(admin.ModelAdmin):
    list_display = ('name','url','PerMethod','argument_list','describe')
@admin.register(Asset)
class asset(admin.ModelAdmin):
    list_display = ('id','device_status','cabinet_num','position','form','AssetNumber','business_unit','latest_date','create_at','administrator')
@admin.register(Server)
class server(admin.ModelAdmin):
    list_display = ('asset_assetnumber','hostname','sn','manufacturer','model','manage_ip','IpAdress','DiskInfo','os_platform','os_version','cpu_count','cpu_physical_count','cpu_model','MemSize','MemNumber','create_at','purchasing_time')
    @staticmethod
    def asset_assetnumber(obj):
        return obj.asset.AssetNumber
@admin.register(NetworkDevice)
class networkdevice(admin.ModelAdmin):
    list_display = ('id','asset_assetnumber','management_ip','intranet_ip','sn','manufacture','model','port_num','device_detail')
    @staticmethod
    def asset_assetnumber(obj):
        return obj.asset.AssetNumber
admin.site.register(models.Permission,usercontrol)
admin.site.register(IDC,idccontrol)
admin.site.register(Per,permission)
