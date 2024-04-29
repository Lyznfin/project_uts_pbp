from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ExcerciseListView, ExcerciseQuestionsView, save_excercise_view, get_time

urlpatterns = [
    path('', ExcerciseListView.as_view()),
    path('<slug:slug>/', ExcerciseQuestionsView.as_view(), name='excercise-detail'),
    path('<slug:slug>/time/', get_time),
    path('<slug:slug>/save/', save_excercise_view, name='save-view')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)