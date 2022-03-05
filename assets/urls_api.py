
from django.urls import path, re_path
from assets import views_api
app_name = 'assets'

urlpatterns = [
    path('business/update/', views_api.business_update, name='business_update'),
    path('business/delete/', views_api.business_delete, name='business_delete'),
    path('business/add/', views_api.business_add, name='business_add'),

    path('idc/add/', views_api.idc_add, name='idc_add'),
    path('idc/update/', views_api.idc_update, name='idc_update'),
    path('idc/delete/', views_api.idc_delete, name='idc_delete'),

    path('server/update/', views_api.server_update, name='server_update'),
    path('server/add/', views_api.server_add, name='server_add'),
    path('server/delete/', views_api.server_delete, name='server_delete'),

]
