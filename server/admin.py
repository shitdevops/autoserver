from django.contrib import admin
from .models import RemoteUser, RemoteUserBindHost, HostGroup
# Register your models here

admin.site.register(RemoteUser)
admin.site.register(RemoteUserBindHost)
admin.site.register(HostGroup)

