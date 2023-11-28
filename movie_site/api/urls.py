from django.urls import path
from . import views

urlpatterns = [
    path('hydrated_data/', views.getData),
    path('hydrated_data_post/', views.addItem),
    path('user_table/', views.getData2),
    path('user_table_post/', views.addItem2),
]