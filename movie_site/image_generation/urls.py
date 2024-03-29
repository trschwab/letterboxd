from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('your-topster.html', views.your_topster, name="your-topster"),
    path('your-stats.html', views.your_stats, name="your-stats"),
    path('your-update.html', views.your_update, name="your-update"),
    path('error.html', views.error, name="error"),
    path('about.html', views.about, name="about"),
]
