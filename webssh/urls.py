
from django.urls import path, re_path
from webssh import views
app_name = 'webssh'

urlpatterns = [
   path('terminal/', views.terminal, name='terminal'),
   path('logs/', views.logs, name='logs'),


   # # 业务线
   # re_path('business_unit/list/$', views.business_unit_list, name='business_unit_list'),
   # re_path('business_unit/add/$', views.business_unit_change, name='business_unit_add'),
   # re_path('business_unit/edit/(\\d+)$', views.business_unit_change, name='business_unit_edit'),
   # re_path('business_unit/delete/$', views.business_unit_change, name='business_unit_delete'),
   #
   # # 主机信息
   # re_path('server/list/$', views.server_list, name='server_list'),
   # re_path('server/detail/(\\d+)/$', views.server_detail, name='server_detail'),
   # # 主机变更记录
   # re_path('server/record/(\\d+)/$', views.server_record, name='server_record'),
   #
   # re_path('server/add/$', views.server_change, name='server_add'),
   # re_path('server/edit/(\\d+)$', views.server_change, name='server_edit'),
   # re_path('server/delete/$', views.server_change, name='server_delete'),
   #
   # # IDC
   # re_path('idc/list/$', views.idc_list, name='idc_list'),
   # re_path('idc/add/$', views.idc_change, name='idc_add'),
   # re_path('idc/edit/(\\d+)$', views.idc_change, name='idc_edit'),
   # re_path('idc/delete/$', views.idc_change, name='idc_delete'),

]
