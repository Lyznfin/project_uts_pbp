from typing import Any
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import CourseExcercise, ExcerciseQuestion, ExcerciseAnswer, ExcerciseResult
from django.views.generic import ListView
from django.views import View

@method_decorator(login_required(login_url='/login' + '?need_account=true'), name='dispatch')
class ExcerciseListView(ListView):
    model = CourseExcercise
    template_name = 'excercise/excercise.html'
    context_object_name = 'excercises'

@method_decorator(login_required(login_url='/login' + '?need_account=true'), name='dispatch')
class ExcerciseQuestionsView(View):
    template_name = 'excercise/excercise.html'

    def get(self, request, slug, *args, **kwargs):
        excercise = get_object_or_404(CourseExcercise, slug=slug)
        excercise_questions = excercise.get_question()
        excercise_duration = excercise.time
        context = {
            'excercise_duration': excercise_duration,
            'excercise_questions': excercise_questions,
            'excercise_name': excercise.name
        }
        return render(request, self.template_name, context)

def get_time(request, slug, *args, **kwargs):
    excercise = CourseExcercise.objects.get(slug=slug)
    return JsonResponse({'time': excercise.time}) 

def save_excercise_view(request, slug, *args, **kwargs):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = request.POST
        data_dict = dict(data.lists())
        data_dict.pop('csrfmiddlewaretoken', None)

        questions = [ExcerciseQuestion.objects.get(pk=key) for key in data_dict.keys()]

        user = request.user
        excercise = CourseExcercise.objects.get(slug=slug)

        multiplier = 100 / excercise.question_count()
        results = []
        correct_answer = None
        score = 0

        for question in questions:
            selected_answer = data_dict.get(f'{question.pk}')

            if selected_answer == ['']:
                results.append({str(question): 'not answered'})
                continue

            answer_pk = int(''.join(selected_answer))
            question_answers = ExcerciseAnswer.objects.filter(question=question.pk)

            for answer in question_answers:
                if not answer.correct:
                    continue

                if answer_pk == answer.pk:
                    score += 1
                
                correct_answer = answer.answer

            your_answer = question_answers.get(pk=answer_pk)
            results.append({str(question): {
                'correct_answer': correct_answer,
                'answered': f'{your_answer.answer}'
                }})
            
        final_score = score * multiplier
        result, created = ExcerciseResult.objects.get_or_create(excercise=excercise, user=user)
        result.score = round(final_score, 0)
        if not created:
            result.save()

        return JsonResponse({'score': round(final_score, 0), 'results': results})
    
    return JsonResponse({'error': 401})