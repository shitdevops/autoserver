from django.contrib import admin
from django.urls import path, include
from api import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # 资产web展示
    path('', include('assets.urls', namespace='assets')),
    path('api/asset/', include('assets.urls_api', namespace='assets_api')),

    # API 资产采集
    path('asset/', views.Asset.as_view()),

    # 登录
    path('user/', include('user.urls', namespace='user')),
    path('api/user/', include('user.urls_api', namespace='user_api')),

    # 主机
    path('server/', include('server.urls', namespace='server')),
    path('api/server/', include('server.urls_api', namespace='server_api')),

    path('webssh/', include('webssh.urls', namespace='webssh')),

    path('batch/', include('batch.urls', namespace='batch')),
    path('api/batch/', include('batch.urls_api', namespace='batch_api')),

]
