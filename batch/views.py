from django.shortcuts import render
from user.tool import login_required
from server.models import HostGroup
from user.models import User
# Create your views here.


@login_required
def cmd(request):
    user = User.objects.get(id=int(request.session.get('userid')))
    groups = HostGroup.objects.filter(user=user)
    print(user, groups)
    return render(request, 'cmd.html', locals())

#
# @login_required
# def script(request):
#     user = User.objects.get(id=int(request.session.get('userid')))
#     groups = HostGroup.objects.filter(user=user)
#     return render(request, 'script.html', locals())
