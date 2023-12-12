from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('your-name.html', views.your_name, name="your-name"),
    path('your-stats.html', views.your_stats, name="your-stats"),
    path('your-update.html', views.your_update, name="your-update"),
]
