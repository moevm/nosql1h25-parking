# nosql_template


## Предварительная проверка заданий

<a href=" ./../../../actions/workflows/1_helloworld.yml" >![1. Согласована и сформулирована тема курсовой]( ./../../actions/workflows/1_helloworld.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/2_usecase.yml" >![2. Usecase]( ./../../actions/workflows/2_usecase.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/3_data_model.yml" >![3. Модель данных]( ./../../actions/workflows/3_data_model.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/4_prototype_store_and_view.yml" >![4. Прототип хранение и представление]( ./../../actions/workflows/4_prototype_store_and_view.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/5_prototype_analysis.yml" >![5. Прототип анализ]( ./../../actions/workflows/5_prototype_analysis.yml/badge.svg)</a> 

<a href=" ./../../../actions/workflows/6_report.yml" >![6. Пояснительная записка]( ./../../actions/workflows/6_report.yml/badge.svg)</a>

<a href=" ./../../../actions/workflows/7_app_is_ready.yml" >![7. App is ready]( ./../../actions/workflows/7_app_is_ready.yml/badge.svg)</a>

## Описание

В рамках проекта по дисциплине «Введение в нереляционные базы данных» в команде 
студентов с помощью MongoDB и Python создана информационная система для оплаты платных 
парковок в Санкт-Петербурге. Сайт позволяет пользователям искать парковки с помощью 
многокритериального фильтра и сортировок, оплачивать их на определённое время, просматривать свои 
оплаты. Привилегия сотрудника даёт возможность просматривать, редактировать и создавать 
пользователей, парковки и оплаты, а также включает в себя массовый импорт и экспорт всех данных 
приложения.

## Стек технологий

Python, Django REST Framework, MongoDB, Nginx, Docker

## Запуск проекта
Находясь в директории репозитория выполнить:
```
docker compose up
```

## Вход
### Админ:
email: admin@admin.ru  
password: password
### Обычный пользователь:
email: test@yandex.ru  
password: testpassword

Ссылка на сайт: http://127.0.0.1:8000
