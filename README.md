# Notification
Web сервис для отправления уведомлений на почту.

## Технологий

## Реализовано

## Установка и запуск
`git clone https://github.com/Kandrey1/notification.git`

`cd notification`

Создать виртуальное окружение командой:
`python -m venv venv`

Установить пакеты:
`python -r requirements.txt`

Запустить контейнер Redis в докере если он не установлен локально:

`docker run -d --name redis -p 6379:6379 redis:7.0.4-alpine3.16`

Запустить worker celery:

`celery -A run.celery worker --loglevel=info --concurrency 4 -P eventlet`

Для мониторинга работы worker celery можно выполнить команду:

`celery -A run.celery flower --loglevel=info`

Приложение запускается по адресу:
`http://127.0.0.1:5000`

## Тестирование

Для тестирования запустить: `pytest tests`

