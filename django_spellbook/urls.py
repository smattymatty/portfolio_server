from django.urls import path
from . import views

urlpatterns = [
    path('test', views.view_test, name='view_test'),
    path('folder1/test1', views.view_folder1_test1, name='view_folder1_test1'),
    path('folder2/test2', views.view_folder2_test2, name='view_folder2_test2')
]