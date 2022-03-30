from django.urls import path
from dollar import views

app_name = 'dollar'

urlpatterns = [
    path('', views.DollarIndexView.as_view(), name='index'),
]
