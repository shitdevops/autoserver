from django.contrib import admin
from repository.models import *
# Register your models here.


admin.site.site_title = '资产管理'
admin.site.site_header = '资产管理'
admin.site.index_title = '资产管理'


admin.site.register(Server)
admin.site.register(BusinessUnit)
admin.site.register(IDC)
admin.site.register(Disk)
admin.site.register(NIC)
admin.site.register(Memory)
admin.site.register(AssetRecord)
