from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse
from jobsearch.models import Specialty, Company, Vacancy

class MainView(View):
    def get(self, request, *args, **kwargs):
        specialyties = Specialty.objects.all()
        companies = Company.objects.all()
        return render(request, 'jobsearch/index.html', context=
                      {
                          'specialyties': specialyties,
                          'companies': companies,
                      })

class VacanciesView(View):
    def get(self, request, *args, **kwargs):
        title = "Все вакансии"
        vacancies = Vacancy.objects.all()
        return render(request, 'jobsearch/vacancies.html', context=
                      {
                          'title': title,
                          'vacancies': vacancies,
                      })

class VacanciesSpesialView(View):
    def get(self, request, code, *args, **kwargs):
        title = Specialty.objects.get(code=code)
        vacancies = Vacancy.objects.filter(specialty=title)
        return render(request, 'jobsearch/vacancies.html', context=
                      {
                          'title': title,
                          'vacancies': vacancies,
                      })

class CompanyView(View):
    def get(self, request, id, *args, **kwargs):
        company = Company.objects.get(id=id)
        vacancies = company.vacancies.all()
        print(vacancies)
        return render(request, 'jobsearch/company.html', context=
                      {
                          'company': company,
                          'vacancies': vacancies,
                      })

class VacancieView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'jobsearch/vacancie.html', context={})
