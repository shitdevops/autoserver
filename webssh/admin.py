from django.contrib import admin
from .models import TerminalLog, TerminalLogDetail
# Register your models here.


admin.site.register(TerminalLog)
admin.site.register(TerminalLogDetail)