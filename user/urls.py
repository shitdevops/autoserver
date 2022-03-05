from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # 登录
    path('login/', views.login, name='login'),
    # 登出
    path('logout/', views.logout, name='logout'),
    # 登录日志
    path('audit/login/', views.audit_login, name='audit_login'),
    # 修改密码
    path('changepasswd/', views.change_passwd, name='changepasswd'),
    # 个人信息
    path('userinfo/', views.user_info, name='userinfo'),
    # 个人信息编辑
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # 用户列表
    path('userlists/', views.user_lists, name='userlists'),
    # 组列表
    path('grouplists/', views.group_lists, name='grouplists'),
    # 组详情
    path('group_detail/<int:group_id>/', views.group_detail, name='group_detail'),
    # 修改组
    path('group_edit/<int:group_id>/', views.group_edit, name='group_edit'),

    # 用户详情
    path('user_detail/<int:user_id>/', views.user_detail, name='user_detail'),
    # 用户信息编辑
    path('user_edit/<int:user_id>/', views.user_edit, name='user_edit'),
    # 添加用户
    path('user_add/', views.user_add, name='user_add'),
    # 添加组
    path('group_add/', views.group_add, name='group_add'),

]
