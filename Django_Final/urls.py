from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include("Accounts.urls")),
    path('',TemplateView.as_view(template_name = "home.html"), name='home'),
    path('dashboard/',include("Services.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)