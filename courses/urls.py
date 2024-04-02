from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Index, UserCourses, AddCourse, RemoveCourse, CourseSectionView, CourseView, AddSection, RemoveSection

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('user', UserCourses.as_view(), name='user-courses'),
    path('<slug:slug>', CourseView.as_view(), name='course-detail'),
    path('<slug:slug>/add', AddCourse.as_view(), name='add-course'),
    path('<slug:slug>/remove', RemoveCourse.as_view(), name='delete-course'),
    path('<slug:slug>/section/<int:pk>', CourseSectionView.as_view(), name='course-section'),
    path('<slug:slug>/section/<int:pk>/add', AddSection.as_view(), name='add-section'),
    path('<slug:slug>/section/<int:pk>/remove', RemoveSection.as_view(), name='delete-section')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)