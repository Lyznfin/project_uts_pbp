from django.contrib import admin
from .models import Instructor, CourseCategory, Course, CoursePrice, CourseSection, UserCourse, CompletedUserSection

admin.site.register(Instructor)
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(CoursePrice)
admin.site.register(CourseSection)
admin.site.register(UserCourse)
admin.site.register(CompletedUserSection)