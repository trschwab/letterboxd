from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('your-name.html', views.your_name, name="your-name"),
]
