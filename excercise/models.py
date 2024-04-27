from django.db import models
from django.utils.text import slugify
from courses.models import Course
from django.contrib.auth.models import User
import random

class CourseExcercise(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="excercises")
    name = models.CharField(max_length=255)
    time = models.IntegerField()
    slug = models.SlugField(default='', blank=True, unique = True, db_index = True)

    def save(self, *args, **kwargs) -> None:
        slug = self.course.title + ' ' + self.name
        self.slug = slugify(slug)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_question(self):
        questions = list(self.questions.all())
        random.shuffle(questions)
        return questions

    def question_count(self):
        return self.questions.count()

class ExcerciseQuestion(models.Model):
    excercise = models.ForeignKey(CourseExcercise, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()

    def __str__(self) -> str:
        return self.question
        
    def get_answers(self):
        return self.answers.all()
    
class ExcerciseAnswer(models.Model):
    question = models.ForeignKey(ExcerciseQuestion, on_delete=models.CASCADE, related_name="answers")
    answer = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer + ' ' + str(self.correct)
    
class ExcerciseResult(models.Model):
    excercise = models.ForeignKey(CourseExcercise, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)

    def __str__(self):
        return f"excercise {self.excercise.name} | score: {self.score}"