from django.urls import path
from .views import MainView, CompanyView, VacanciesSpesialView, VacanciesView, VacancieView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:code>', VacanciesSpesialView.as_view(), name='special_vacancies'),
    path('companies/<int:id>', CompanyView.as_view(), name='company'),
    path('vacancies/<int:id>', VacancieView.as_view(), name='vacancie'),
]
