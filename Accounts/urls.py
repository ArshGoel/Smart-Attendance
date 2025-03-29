from django.conf import settings
from django.contrib import admin
from django.urls import path
from Accounts import views
from django.conf.urls.static import static

urlpatterns = [
    path('slogin',views.slogin,name="slogin"),
    path('tlogin',views.tlogin,name="tlogin"),
    path('logout',views.logout,name="logout"),
    path('preview-users/', views.preview_users, name='preview_users'),
    path('import-users/', views.import_users, name='import_users'),
    path('profile/', views.profile, name='profile'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
