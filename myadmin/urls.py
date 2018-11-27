from django.urls import path, include
from. import views

app_name = 'myadmin'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('edit/<forloop_counter>', views.edit, name='edit'),
    path('del/<forloop_counter>', views.delete, name='del'),
    path('cross/<forloop_counter>', views.cross, name='cross'),
    path('savecloud_from_text/', views.savecloud_from_text,
         name='savecloud_from_text'),
    path('check_saveonecloud', views.check_saveonecloud, name='check_saveonecloud'),
]
