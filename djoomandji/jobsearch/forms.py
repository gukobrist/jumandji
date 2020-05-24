from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone

from .models import Application, Company, Vacancy, Resume


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        widgets = {
            'written_username': forms.TextInput(attrs={
                'class': "form-control",
                'id': "userName",
            }),
            'written_phone': forms.NumberInput(attrs={
                'class': "form-control",
                'id': "userPhone",
                'placeholder': "79999999999",
            }),
            'written_cover_letter': forms.Textarea(attrs={
                'class': "form-control",
                'id': "userMsg",
                'rows': "8",
            })
        }

    def save(self, request, id):
        Application.objects.create(
            user = request.user,
            vacancy = Vacancy.objects.get(id=id),
            written_username = self.cleaned_data['written_username'],
            written_phone = self.cleaned_data['written_phone'],
            written_cover_letter = self.cleaned_data['written_cover_letter'],
        )

class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class':"form-control",
            'id':"inputEmail",
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class':"form-control",
            'id':"inputPassword",
        })
    )


class SigupForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class':"form-control",
            'id':"inputUsername",
        }),
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class':"form-control",
            'id':"inputFirstName",
        }),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class':"form-control",
            'id':"inputLastName",
        }),
    )
    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class':"form-control",
            'id':"inputEmail",
        }),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class':"form-control",
            'id':"inputPassword",
        }),
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class':"form-control",
            'id':"InputRepeatPassword",
        }),
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'location', 'description', 'employee_count',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'id': "companyName",
            }),
            'location': forms.TextInput(attrs={
                'class': "form-control",
                'id': "companyLocation",
            }),
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'id': "companyInfo",
                'rows': "4"
            }),
            'employee_count': forms.TextInput(attrs={
                'class': "form-control",
                'id': "companyTeam",
            })
        }
    def save(self, request):
        if len(request.FILES) != 0:
            logo = "/company_images/" + str(request.FILES['logo'])
        else:
            try:
                logo =  Company.objects.get(owner=request.user).logo
            except:
                logo = None
        obj, created = Company.objects.update_or_create(
            owner=request.user,
            defaults={
                'name': self.cleaned_data['name'],
                'location': self.cleaned_data['location'],
                'description': self.cleaned_data['description'],
                'employee_count': self.cleaned_data['employee_count'],
                'logo': logo,
            },
        )

class ResumeForm(forms.ModelForm):

    class Meta:
        model = Resume
        fields = (
            'name', 'surname', 'status', 'status', 'salary', 'specialty', 'grade',
            'education', 'expirience', 'portfolio',
        )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'id': "userName",
            }),
            'surname': forms.TextInput(attrs={
                'class': "form-control",
                'id': "userSurname",
            }),
            'status':  forms.Select(attrs={
                'class': "form-control",
                'id': "userReady",
            }),
            'salary': forms.NumberInput(attrs={
                'class': "form-control",
                'id': "userSalary",
            }),
            'specialty': forms.Select(attrs={
                'class': "form-control",
                'id': "userSpecialization",
            }),
            'grade': forms.Select(attrs={
                'class': "form-control",
                'id': "userQualification",
            }),
            'education': forms.Textarea(attrs={
                'class': "form-control",
                'id': "userEducation",
                'rows': "4",
            }),
            'expirience': forms.Textarea(attrs={
                'class': "form-control",
                'id': "userExperience",
                'rows': "4",
            }),
            'portfolio': forms.TextInput(attrs={
                'class': "form-control",
                'id': "userPortfolio",
            }),
        }

    def save(self, request):
        obj, created = Resume.objects.update_or_create(
            user=request.user,
            defaults={
                'name': self.cleaned_data['name'],
                'surname': self.cleaned_data['surname'],
                'status': self.cleaned_data['status'],
                'salary': self.cleaned_data['salary'],
                'specialty': self.cleaned_data['specialty'],
                'grade': self.cleaned_data['grade'],
                'education': self.cleaned_data['education'],
                'expirience': self.cleaned_data['expirience'],
                'portfolio': self.cleaned_data['portfolio'],
            },
        )



class VacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max',)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
                'id':"vacancyTitle",
            }),
            'specialty': forms.Select(attrs={
                'class': "form-control",
                'id':"userSpecialization",
            }),
            'skills': forms.Textarea(attrs={
                'class': "form-control",
                'id':"vacancySkills",
                'rows': "3",
            }),
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'id':"vacancyDescription",
                'rows': "13",

            }),
            'salary_min': forms.NumberInput(attrs={
                'class': "form-control",
                'id':"vacancySalaryMin",
            }),
            'salary_max': forms.NumberInput(attrs={
                'class': "form-control",
                'id':"vacancySalaryMax",
            }),
        }
    def save(self, request, id):
        company = Company.objects.get(owner=request.user)
        obj, created = Vacancy.objects.update_or_create(
            id=id,
            defaults={
                'title': self.cleaned_data  ['title'],
                'specialty': self.cleaned_data['specialty'],
                'company': company,
                'skills': self.cleaned_data['skills'],
                'description': self.cleaned_data['description'],
                'salary_max': self.cleaned_data['salary_max'],
                'salary_min': self.cleaned_data['salary_min'],
                'published_at': timezone.now(),
            },
        )
