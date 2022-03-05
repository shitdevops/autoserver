from django.urls import path, re_path
from . import views

app_name = 'server'

urlpatterns = [
    # 主机列表
    path('host_lists/', views.host_lists, name='host_lists'),
    # 主机详情
    path('host_detail/<int:host_id>/', views.host_detail, name='host_detail'),
    # 主机添加
    path('host_add/', views.host_add, name='host_add'),
    # 主机编辑
    path('host/<int:host_id>/edit/', views.host_edit, name='host_edit'),

    # 主机用户列表
    path('host_users/', views.host_users, name='host_users'),
    # 主机用户添加
    path('user_add/', views.user_add, name='user_add'),
    # 主机用户详情
    path('user_detail/<int:user_id>/', views.user_detail, name='user_detail'),
    # 主机用户编辑
    path('user/<int:user_id>/edit', views.user_edit, name='user_edit'),

    # 主机组列表
    path('host_groups/', views.host_groups, name='host_groups'),
    # 主机组详情
    path('host_groups_detail/<int:groups_id>', views.host_groups_detail, name='host_groups_detail'),
    # 主机组修改
    path('host_groups_edit/<int:group_id>', views.host_groups_edit, name='host_groups_edit'),
    # 主机组添加
    path('host_groups_add', views.host_groups_add, name='host_groups_add'),
]
