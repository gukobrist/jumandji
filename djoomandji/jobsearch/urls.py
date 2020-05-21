from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from .views import MainView, CompanyView, VacanciesSpesialView, VacanciesView
from .views import VacancyView, VacancySendView, MyCompanyView, MyVacanciesView
from .views import OneMyVacancyView, LoginView, SignupView, MyCompanyNewView
from .views import MyVacancyNewView, VacancyApplicationsView


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('vacancies', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:code>', VacanciesSpesialView.as_view(), name='special_vacancies'),
    path('companies/<int:id>', CompanyView.as_view(), name='company'),
    path('vacancies/<int:id>', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:id>/send', VacancySendView.as_view(), name='send_vacancy',),
    path('mycompany/', MyCompanyView.as_view(), name='my_company',),
    path('mycompany/new', MyCompanyNewView.as_view(), name='new_company',),
    path('mycompany/vacancies', MyVacanciesView.as_view(), name='my_vacancies'),
    path('mycompany/vacancies/new', MyVacancyNewView.as_view(), name='new_vacancy'),
    path('mycompany/vacancies/<int:id>', OneMyVacancyView.as_view(), name='one_vacancy'),
    path('mycompany/vacancies/applications/<int:id>', VacancyApplicationsView.as_view(), name='vacancy_applications',),
    path('login/', LoginView.as_view(), name='login',),
    path('signup/', SignupView.as_view(), name='signup',),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout',),
]
