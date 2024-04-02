from django import forms
from .models import UserCourse

class UserCourseForm(forms.ModelForm):
    class Meta:
       model = UserCourse
       fields = []