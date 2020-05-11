from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import View

from jobsearch.models import Specialty, Company, Vacancy


class MainView(View):
    def get(self, request, *args, **kwargs):
        specialyties = get_list_or_404(Specialty)
        companies = get_list_or_404(Company)
        return render(request, 'jobsearch/index.html', context={
            'specialyties': specialyties,
            'companies': companies,
        })


class VacanciesView(View):
    def get(self, request, *args, **kwargs):
        title = "Все вакансии"
        vacancies = get_list_or_404(Vacancy)
        return render(request, 'jobsearch/vacancies.html', context={
            'title': title,
            'vacancies': vacancies,
        })


class VacanciesSpesialView(View):
    def get(self, request, code, *args, **kwargs):
        title = Specialty.objects.get(code=code)
        vacancies = get_list_or_404(Vacancy, specialty=title)
        return render(request, 'jobsearch/vacancies.html', context={
            'title': title,
            'vacancies': vacancies,
        })


class CompanyView(View):
    def get(self, request, id, *args, **kwargs):
        company = get_object_or_404(Company, id=id)
        vacancies = company.vacancies.all()
        referrer = request.META.get('HTTP_REFERER', '/')
        return render(request, 'jobsearch/company.html', context={
            'company': company,
            'vacancies': vacancies,
            'referrer': referrer,
        })


class VacancyView(View):
    def get(self, request, id, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, id=id)
        referrer = request.META.get('HTTP_REFERER', '/')
        return render(request, 'jobsearch/vacancie.html', context={
            'vacancy': vacancy,
            'referrer': referrer,
        })
