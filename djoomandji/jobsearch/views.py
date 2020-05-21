from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, Http404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages

from jobsearch.models import Specialty, Company, Vacancy, Application
from .forms import ApplicationForm, LoginForm, SigupForm, CompanyForm, VacancyForm


class MainView(View):
    def get(self, request, *args, **kwargs):
        try:
            specialyties = Specialty.objects.all()
            companies = Company.objects.all()
        except:
            raise Http404("Такого не существует")
        return render(request, 'jobsearch/index.html', context={
            'specialyties': specialyties,
            'companies': companies,
        })


class VacanciesView(View):
    def get(self, request, *args, **kwargs):
        title = "Все вакансии"
        try:
            vacancies = Vacancy.objects.all()
        except:
            raise Http404('Нет ни одной вакансии')
        return render(request, 'jobsearch/vacancies.html', context={
            'title': title,
            'vacancies': vacancies,
            'vacancies_count': vacancies.count(),
        })


class VacanciesSpesialView(View):
    def get(self, request, code, *args, **kwargs):
        try:
            title = Specialty.objects.get(code=code)
            vacancies = Vacancy.objects.filter(specialty=title)
        except:
            raise Http404('Такой страницы не существует')
        return render(request, 'jobsearch/vacancies.html', context={
            'title': title,
            'vacancies': vacancies,
            'vacancies_count': vacancies.count(),
        })


class CompanyView(View):
    def get(self, request, id, *args, **kwargs):
        company = get_object_or_404(Company, id=id)
        vacancies = company.vacancies.all()
        return render(request, 'jobsearch/company.html', context={
            'company': company,
            'vacancies': vacancies,
            'vacancies_count': vacancies.count()
        })


class VacancyView(View):
    def get(self, request, id, *args, **kwargs):
        try:
            vacancy = Vacancy.objects.get(id=id)
            form = ApplicationForm()
        except:
            raise Http404('Такой вакансии нет')
        return render(request, 'jobsearch/vacancie.html', context={
            'vacancy': vacancy,
            'form': form,
        })


class VacancySendView(View):
    def post(self, request, id, *args, **kwargs):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save(request, id)
            return render(request, 'jobsearch/sent.html', context={
        })


class MyCompanyView(View):
    def get(self, request, *args, **kwargs):
        try:
            form = CompanyForm(instance=request.user.company)
            return render(request, 'jobsearch/company-edit.html', context={
                'form': form,
                'logo': request.user.company.logo,
            })
        except:
            return render(request, 'jobsearch/company-create.html', context={})

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/mycompany')
        return render(request, 'jobsearch/company-edit.html', context={
            'form': form,
            'logo': request.user.company.logo,
        })


class MyCompanyNewView(View):
    def get(self, request, *args, **kwargs):
        form = CompanyForm()
        return render(request, 'jobsearch/company-edit.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/mycompany/new')
        return render(request, 'jobsearch/company-edit.html', context={
            'form': form,
        })


class MyVacanciesView(View):
    def get(self, request, *args, **kwargs):
        try:
            vacancies = Vacancy.objects.filter(company=request.user.company)
        except:
            return HttpResponseRedirect('/mycompany/')
        return render(request, 'jobsearch/vacancy-list.html', context={
            'vacancies': vacancies,
        })


class MyVacancyNewView(View):
    def get(self, request, *args, **kwargs):
        form = VacancyForm()
        return render(request, 'jobsearch/vacancy-new.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save(request, None)
            return HttpResponseRedirect('/mycompany/vacancies')
        return render(request, 'jobsearch/vacancy-new.html', context={
            'form': form,
        })


class OneMyVacancyView(View):
    def get(self, request, id, *args, **kwargs):
        vacancy = Vacancy.objects.get(id=id)
        applications = vacancy.applications.all()
        form = VacancyForm(instance=vacancy)
        return render(request, 'jobsearch/vacancy-edit.html', context={
            'form': form,
            'vacancy': vacancy,
            'applications_count': applications.count(),
            'applications': applications,
        })

    def post(self, request, id, *args, **kwargs):
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save(request, id)
            return HttpResponseRedirect('/mycompany/vacancies')
        return render(request, 'jobsearch/vacancy-edit.html', context={
            'form': form,
            'vacancy': vacancy,
            'applications_count': applications.count(),
            'applications': applications,
        })


class VacancyApplicationsView(View):
    def get(self, request, id, *args, **kwargs):
        vacancy = Vacancy.objects.get(id=id)
        applications = vacancy.applications.all()
        return render(request, 'jobsearch/vacancy-applications.html', context={
            'applications': applications,
            'applications_count': applications.count(),
        })


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'jobsearch/login.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            username = User.objects.get(email=email.lower()).username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'jobsearch/login.html', context={
            'form': form,
        })


class SignupView(View):
    def get(self, request, *args, **kwargs):
        form = SigupForm()
        return render(request, 'jobsearch/register.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SigupForm(request.POST)
        if form.is_valid():
            print(1)
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'jobsearch/register.html', context={
            'form': form,
        })
