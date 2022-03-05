from django.shortcuts import render
from user.tool import login_required, admin_required
from .forms import HostForm
from user.models import RemoteUserBindHost
from .models import TerminalLog
from django.http import JsonResponse
# Create your views here.


@login_required
def terminal(request):
    host_form = HostForm(request.POST)
    error_message = '请检查填写的内容!'
    if host_form.is_valid():
        host_id = host_form.cleaned_data.get('hostid')
        host = RemoteUserBindHost.objects.get(id=host_id)
        return render(request, 'webssh/terminal.html', locals())

    return JsonResponse({"code": 406, "err": error_message})


@admin_required
@login_required
def logs(request):
    logs = TerminalLog.objects.all()
    return render(request, 'webssh/terminal_logs.html', locals())