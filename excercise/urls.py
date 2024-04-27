from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ExcerciseListView, ExcerciseQuestionsView

urlpatterns = [
    path('', ExcerciseListView.as_view()),
    path('<slug:slug>/', ExcerciseQuestionsView.as_view(), name='excercise-detail')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)