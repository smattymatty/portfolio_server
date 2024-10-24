from django.urls import path
from . import views

urlpatterns = [
    path('test', views.view_test, name='view_test'),
    path('folder_1/test_span', views.view_folder_1_test_span,
         name='view_folder_1_test_span'),
    path('folder_1/test_1', views.view_folder_1_test_1,
         name='view_folder_1_test_1'),
    path('folder_1/subfolder1/hey', views.view_folder_1_subfolder1_hey,
         name='view_folder_1_subfolder1_hey'),
    path('spells/my_spells', views.view_spells_my_spells,
         name='view_spells_my_spells')
]
