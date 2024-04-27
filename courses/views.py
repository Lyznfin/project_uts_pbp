from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Course, CourseSection, UserCourse, CourseCategory, CompletedUserSection
from django.db.models import Q
from django.utils import timezone

class Index(ListView):
    template_name = 'courses/index.html'
    model = Course
    context_object_name = 'courses'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        durations = self.request.GET.getlist('duration')
        categories = self.request.GET.getlist('category')

        if durations and categories:
            duration_filter = self.get_duration_filter(durations)
            category_filter = self.get_category_filter(categories)
            queryset = queryset.filter(duration_filter & category_filter)
        elif durations:
            queryset = queryset.filter(self.get_duration_filter(durations))
        elif categories:
            queryset = queryset.filter(self.get_category_filter(categories))

        queryset = queryset.distinct()
        return queryset

    def get_duration_filter(self, durations):
        duration_filters = []
        for duration in durations:
            if duration == '1':
                duration_filters.append(Q(duration__lt=timezone.timedelta(minutes=30)))
            elif duration == '2':
                duration_filters.append(Q(duration__range=(timezone.timedelta(minutes=30), timezone.timedelta(minutes=60))))
            elif duration == '3':
                duration_filters.append(Q(duration__range=(timezone.timedelta(hours=1), timezone.timedelta(hours=2))))
            elif duration == '4':
                duration_filters.append(Q(duration__range=(timezone.timedelta(hours=2), timezone.timedelta(hours=5))))
            elif duration == '5':
                duration_filters.append(Q(duration__range=(timezone.timedelta(hours=5), timezone.timedelta(hours=10))))
            elif duration == '6':
                duration_filters.append(Q(duration__gte=timezone.timedelta(hours=10)))
        q_objects = Q()
        for q_obj in duration_filters:
            q_objects |= q_obj
        return q_objects
    
    def get_category_filter(self, categories):
        category_filters = []
        for category in categories:
            category_filters.append(Q(categories__pk=category))
        q_objects = Q()
        for q_obj in category_filters:
            q_objects |= q_obj
        return q_objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for course in context['courses']:
            total_seconds = course.duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            course.duration_hours = hours
            course.duration_minutes = minutes
        context['categories'] = self.get_all_category()
        context['selected_durations'] = self.request.GET.getlist('duration')
        context['selected_categories'] = self.request.GET.getlist('category')
        return context
    
    def get_all_category(self):
        list_category = CourseCategory.objects.all()
        return list_category

class CourseView(View):
    template_name = 'courses/course.html'
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        first_section = course.coursesection_set.first()
        return redirect('course-section', slug=slug, pk=first_section.pk)

class AddCourse(View):
    @method_decorator(login_required(login_url='/login?need_account=true'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, slug):
        user = request.user
        course = get_object_or_404(Course, slug=slug)
        user_course = UserCourse.objects.create(user=user, course=course)
        user_course.save()
        return redirect('course-detail', slug=slug)

class RemoveCourse(View):
    @method_decorator(login_required(login_url='/login?need_account=true'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, slug):
        user = request.user
        course = get_object_or_404(Course, slug=slug)
        user_course = get_object_or_404(UserCourse, user=user, course=course)
        user_course.delete()
        return redirect('course-detail', slug=slug)

class CourseSectionView(View):
    template_name = 'courses/course.html'

    @method_decorator(login_required(login_url='/login?need_account=true'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, slug, pk):
        course = get_object_or_404(Course, slug=slug)
        sections = CourseSection.objects.filter(course=course)
        section = get_object_or_404(sections, pk=pk)
        user = self.request.user
        if user.is_authenticated:
            user_added_course = UserCourse.objects.filter(user=user, course=course).exists()
            completed_sections = user.completedusersection_set.all()
            completed_sections = [completed.get("section") for completed in completed_sections.values("section")]
            context = {
                'course': course,
                'sections': sections,
                'section': section,
                'user_added_course': user_added_course,
                'completed_sections': completed_sections
            }
        else:
            user_added_course = False
            context = {
                'course': course,
                'sections': sections,
                'section': section,
                'user_added_course': user_added_course
            }
        return render(request, self.template_name, context=context)

class AddSection(View):
    @method_decorator(login_required(login_url='/login?need_account=true'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, slug, pk):
        user = request.user
        section = get_object_or_404(CourseSection, pk=pk)
        user_section = CompletedUserSection.objects.create(user=user, section=section)
        user_section.save()
        return redirect('course-section', slug=slug, pk=pk)

class RemoveSection(View):
    @method_decorator(login_required(login_url='/login?need_account=true'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, slug, pk):
        user = request.user
        section = get_object_or_404(CourseSection, pk=pk)
        user_section = CompletedUserSection.objects.get(user=user, section=section)
        user_section.delete()
        return redirect('course-section', slug=slug, pk=pk)
    
@method_decorator(login_required(login_url='/login' + '?need_account=true'), name='dispatch')
class UserCourses(ListView):
    template_name = 'courses/user-course.html'
    model = UserCourse
    context_object_name = 'usercourses'
    paginate_by = 5

    def get_queryset(self):
        usercourse = super().get_queryset()
        return usercourse.filter(user=self.request.user)    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        usercourses = context.get("usercourses")
        completed_sections = CompletedUserSection.objects.filter(user=user)
        completed_sections = [section.section.pk for section in completed_sections]
        for usercourse in usercourses:
            usercourse.total_sections = [section.get('pk') for section in usercourse.course.coursesection_set.values('pk')]
            usercourse.completed_sections = 0
            for section in usercourse.total_sections:
                if section in completed_sections:
                    usercourse.completed_sections += 1
        return context
