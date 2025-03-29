from django.contrib import admin
from django.urls import path
from Services import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('student',views.student,name="student"),
    path('teacher',views.teacher,name="teacher"),
    path('not_allowed',views.not_allowed,name="not_allowed"),
    path('capture/', views.capture_image, name='capture_image'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('stop_camera/', views.stop_camera, name='stop_camera'),
    path('view_student',views.view_student, name='view_student'),
    path('users/<str:username>/images/', views.view_images, name='view_images'),
    path('users/<str:username>/train/', views.train_images, name='train_images'),

    path('train_all_images/', views.train_all_images, name='train_all_images'),
    
    path('attendance/', views.attendance, name='attendance'),
    path('save_attendance', views.save_attendance, name='save_attendance'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
