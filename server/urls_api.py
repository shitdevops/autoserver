from django.urls import path
from . import views_api

app_name = 'server'

urlpatterns = [
    path('host/add/', views_api.host_add, name='host_add'),
    path('host/update/', views_api.host_update, name='host_update'),
    path('host/delete/', views_api.host_delete, name='host_delete'),

    path('user/add/', views_api.user_add, name='user_add'),
    path('user/update/', views_api.user_update, name='user_update'),
    path('user/delete/', views_api.user_delete, name='user_delete'),

    path('group/delete/', views_api.host_group_delete, name='host_group_delete'),
    path('group/update/', views_api.host_group_update, name='host_group_update'),
    path('group/add/', views_api.host_group_add, name='host_group_add'),
]
