from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User

class Instructor(models.Model):
    username = models.CharField(max_length = 25, unique = True)
    youtube = models.URLField(max_length = 100, unique = True)

    def __str__(self):
        return f"{self.username}"

class CourseCategory(models.Model):
    class Categories(models.TextChoices):
        PYTHON = 'PY', _('Python')
        RUST = 'RS', _('Rust')
        JAVA = 'JV', _('Java')
        JAVASCRIPT = 'JS', _('JavaScript')
        C_SHARP = 'CS', _('C#')
        C_PLUS_PLUS = 'CPP', _('C++')
        HTML_CSS = 'HTSS', _('HTML/CSS')
        REACT = 'REA', _('React')
        ANGULAR = 'ANG', _('Angular')
        VUE = 'VUE', _('Vue.js')
        PHP = 'PHP', _('PHP')
        SWIFT = 'SW', _('Swift')
        KOTLIN = 'KT', _('Kotlin')
        GO = 'GO', _('Go')
        RUBY = 'RB', _('Ruby')
        SQL = 'SQL', _('SQL')
        MACHINE_LEARNING = 'ML', _('Machine Learning')
        DATA_SCIENCE = 'DS', _('Data Science')
        DATA_STRUCTURE_ALGORITHM = 'DSA', _('Data Structure and Algorithm')
        ARTIFICIAL_INTELLIGENCE = 'AI', _('Artificial Intelligence')
        BLOCKCHAIN = 'BC', _('Blockchain')
        DEVOPS = 'DO', _('DevOps')
        CLOUD_COMPUTING = 'CC', _('Cloud Computing')
        BACKEND = 'BE', _('Backend Development')
        FRONTEND = 'FE', _('Frontend Development')
        GAME_DEVELOPMENT = 'GAME', _('Game Development')
        MOBILE_DEVELOPMENT = 'MOB', _('Mobile App Development')
        WEB_DEVELOPMENT = 'WEB', _('Web Development')
        UI_UX = 'UIUX', _('UI/UX Design')
        DATABASES = 'DB', _('Databases')
        SECURITY = 'SEC', _('Cyber Security')
        NO_SQL = 'NSQL', _('No SQL')
    category = models.CharField(max_length = 4, choices = Categories.choices, unique = True)

    def get_category_name(self):
        return dict(self.Categories.choices)[self.category]

    def __str__(self):
        return str(self.get_category_name())

class Course(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100, unique = True)
    description = models.TextField(max_length = 300)
    slug = models.SlugField(default='', blank=True, unique = True, db_index = True)
    duration = models.DurationField()
    published = models.DateField(default=timezone.now)
    categories = models.ManyToManyField(CourseCategory)

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("course-detail", kwargs = {"slug": self.slug})
    
    def __str__(self):
        return f"{self.title}"

class CourseSection(models.Model):
    class Meta:
        unique_together = ('course', 'section')

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.CharField(max_length = 100)
    pointer = models.TextField(max_length = 400)

    def get_absolute_url(self):
        return reverse("course-section", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f"{self.section}"

class UserCourse(models.Model):
    class Meta:
        unique_together = ('user', 'course')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.course.title}'

class CompletedUserSection(models.Model):
    class Meta:
        unique_together = ('user', 'section')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}: {self.section.section}'

class CoursePrice(models.Model):
    course = models.OneToOneField(Course, on_delete = models.CASCADE)
    paid_type = models.CharField(max_length=1, choices = [('F', 'Free'), ('P', 'Paid')], default='F')
    price = models.DecimalField(decimal_places = 2, max_digits = 8, validators=[MinValueValidator(0)], default = 0)

    def clean(self):
        if self.paid_type == 'F' and self.price != 0:
            raise ValidationError('Price must be 0 for a free course')
        elif self.paid_type == 'P' and self.price == 0:
            raise ValidationError('Price must be set for a paid course')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_price(self):
        if self.paid_type == 'F':
            return 'Free'
        else:
            return f'{self.price}$'

    def __str__(self):
        return f"{self.course}: {self.get_price()}"


