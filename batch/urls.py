from django.urls import path
from . import views


app_name = "batch"
urlpatterns = [
    path('cmd/', views.cmd, name='cmd'),
    # path('script/', views.script, name='script'),
]

