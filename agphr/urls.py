from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .utils.views import RootView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('job.urls', namespace='job')),
    path('users/', include('users.urls', namespace='users')),
    path('redirect/', RootView.as_view(), name='redirect_url'),
    path('super_admin/', include('super_admin.urls', namespace='super_admin')),
    path('employer/', include('employer.urls', namespace='employer')),
    path('applicant/', include('applicant.urls', namespace='applicant')),
    path('tinymce/', include('tinymce.urls')),
    path('quiz/', include('quiz.urls', namespace='quiz')),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)