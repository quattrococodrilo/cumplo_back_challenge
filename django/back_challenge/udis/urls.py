from django.urls import path
from udis import views

app_name = 'udis'

urlpatterns = [
    path('', views.UdisFormView.as_view(), name='index'),
]
