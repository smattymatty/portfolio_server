from django.urls import path
from . import views

urlpatterns = [
    path('introduction', views.view_introduction, name='view_introduction'),
    path('djangolike', views.view_djangolike, name='view_djangolike'),
    path('spellbook/sb_intro', views.view_spellbook_sb_intro, name='view_spellbook_sb_intro')
]