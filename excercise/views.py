from typing import Any
from django.shortcuts import render, get_object_or_404
from .models import CourseExcercise, ExcerciseQuestion
from django.views.generic import ListView
from django.views import View
from django.core.paginator import Paginator

class ExcerciseListView(ListView):
    model = CourseExcercise
    template_name = 'excercise/excercise.html'
    context_object_name = 'excercises'

class ExcerciseQuestionsView(View):
    template_name = 'excercise/excercise.html'

    def get(self, request, slug, *args, **kwargs):
        excercise = get_object_or_404(CourseExcercise, slug=slug)
        excercise_questions = excercise.get_question()
        paginator = Paginator(excercise_questions, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        last_page_number = paginator.num_pages - 1 if paginator.num_pages > 0 else 0
        is_last_page = True if last_page_number == page_obj.number - 1 else False
        context = {
            'excercise_questions': page_obj,
            'excercise_name': excercise.name,
            'has_pagination': paginator.num_pages > 1,
            'is_last_page': is_last_page
        }
        return render(request, self.template_name, context)