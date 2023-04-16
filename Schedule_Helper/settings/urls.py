from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from backend import views
from django.urls import path, include
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet, basename='MyModel')
router.register(r'profiles', views.ProfileViewSet)
router.register(r'schedule', views.ScheduleViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
