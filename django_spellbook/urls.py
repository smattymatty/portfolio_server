from django.urls import path
from . import views

urlpatterns = [
    path('introduction', views.view_introduction, name='view_introduction'),
    path('djangolike', views.view_djangolike, name='view_djangolike')
]