from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from .views import 

urlpatterns = [
    # path('<slug:slug>', CourseView.as_view(), name='course-detail')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)