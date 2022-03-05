
from django.urls import path, re_path
from assets import views
app_name = 'assets'

urlpatterns = [
   # 首页
   path('', views.dashboard, name='dashboard'),
   # 资产列表
   path('server/', views.server, name='server'),
   # 资产变更记录
   path('server-record/<int:asset_id>/', views.server_record, name='server_record'),
   # 资产修改
   path('server/<int:asset_id>/', views.server_edit, name='server_edit'),
   # 资产详情
   path('server/<int:asset_id>/detail/', views.server_detail, name='server_detail'),
   # 资产添加
   path('server/add/', views.server_add, name='server_add'),
   # re_path('detail/(\\d+)$', views.detail, name='detail'),
   # re_path('server-add/', views.server_add, name='server_add'),
   # re_path('server/edit/$', views.server_edit, name='server_edit'),

   # 业务线
   path('business_unit/list/', views.business_unit_list, name='business_unit_list'),
   # 业务线修改
   path('business/<int:business_id>/', views.business_edit, name='business_edit'),
   # 业务线详情
   path('business/<int:business_id>/detail/', views.business_detail, name='business_detail'),
   # 业务线添加
   path('business/add/', views.business_add, name='business_add'),

   # ICD机房
   path('idc/list/', views.idc_list, name='idc_list'),
   # IDC详情
   path('idc/<int:idc_id>/detail/', views.idc_detail, name='idc_detail'),
   # IDC添加
   path('idc/add/', views.idc_add, name='idc_add'),
   # IDC编辑
   path('idc/<int:idc_id>/', views.idc_edit, name='idc_edit'),
]
