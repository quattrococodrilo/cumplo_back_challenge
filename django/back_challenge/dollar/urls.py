from django.urls import path
from udis import views

app_name = 'dollar'

urlpatterns = [
    path('', views.UdisIndexView.as_view(), name='index'),
]
