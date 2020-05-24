from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=settings.MEDIA_COMPANY_IMAGE_DIR, blank=True, null=True)
    description = models.TextField()
    employee_count = models.IntegerField(null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class Specialty(models.Model):
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR,)

    def __str__(self):
        return self.title

class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()

    def __str__(self):
        return self.title

class Application(models.Model):
    written_username = models.CharField(max_length=100)
    written_phone = models.IntegerField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return self.written_username



class Resume(models.Model):
    STATUS_CHOICES = [
        ('no', 'Не ищу работу'),
        ('maybe', 'Рассматриваю предложения'),
        ('yes', 'Ищу работу'),
    ]
    GRADE_CHOICES = [
        ('intern', 'Стажер'),
        ('junior', 'Джуниор'),
        ('moddle', 'Мидл'),
        ('senior', 'Синьор'),
        ('lead', 'Лид'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS_CHOICES, default=None, max_length=100)
    salary = models.IntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='resume')
    grade = models.CharField(choices=GRADE_CHOICES, default=None, max_length=100)
    education = models.CharField(max_length=100)
    expirience = models.CharField(max_length=100)
    portfolio = models.CharField(max_length=100)

    def __str__(self):
        return self.name
