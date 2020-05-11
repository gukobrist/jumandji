from django.core.management.base import BaseCommand

from jobsearch.models import Company, Specialty, Vacancy

""" Вакансии """

jobs = [

    {"title": "Разработчик на Python", "cat": "backend", "company": "staffingsmarter", "salary_from": "100000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик в проект на Django", "cat": "backend", "company": "swiftattack", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик на Swift в аутсорс компанию", "cat": "backend", "company": "swiftattack",
     "salary_from": "120000", "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Мидл программист на Python", "cat": "backend", "company": "workiro", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Питонист в стартап", "cat": "backend", "company": "primalassault", "salary_from": "120000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"}

]

""" Компании """

companies = [

    {"title": "workiro"},
    {"title": "rebelrage"},
    {"title": "staffingsmarter"},
    {"title": "evilthreath"},
    {"title": "hirey"},
    {"title": "swiftattack"},
    {"title": "troller"},
    {"title": "primalassault"}

]

""" Категории """

specialties = [

    {"code": "frontend", "title": "Фронтенд"},
    {"code": "backend", "title": "Бэкенд"},
    {"code": "gamedev", "title": "Геймдев"},
    {"code": "devops", "title": "Девопс"},
    {"code": "design", "title": "Дизайн"},
    {"code": "products", "title": "Продукты"},
    {"code": "management", "title": "Менеджмент"},
    {"code": "testing", "title": "Тестирование"}

]


class Command(BaseCommand):
    help = 'This command need for populating bd from data.py file'

    def _creat_companies(self):
        for i in companies:
            company = Company(name=i['title'])
            company.save()

    def _create_specialties(self):
        for i in specialties:
            spesialty = Specialty(code=i['code'], title=i['title'])
            spesialty.save()

    def _create_vacancies(self):
        for i in jobs:
            vacancy = Vacancy(title=i['title'], specialty=Specialty.objects.get(code=i['cat']),
                              company=Company.objects.get(name=i['company']), salary_min=i['salary_from'],
                              salary_max=i['salary_to'], published_at=i['posted'], description=i['desc'])
            vacancy.save()

    def handle(self, *args, **kwargs):
        self._creat_companies()
        self._create_specialties()
        self._create_vacancies()

        self.stdout.write(self.style.SUCCESS('DataBase successfully populated'))
