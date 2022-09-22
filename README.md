# Notification
Web сервис для отправления уведомлений на почту.

## Технологий

## Реализовано

---

###Добавление нового клиента.
 - api/client - добавление и удаление нового клиента.

    - Для добавления методом POST передается json {"email":, "tag":}

    - Для удаления методом DELETE передается json {"id_delete":}


 - api/client/<id_update> - обновление данных клиента с id=<id_update>

    - Для обновления методом PUT передается json {"up_email":, "up_tag":}
---
###Добавление новой рассылки.

 - api/mailing - добавление и удаление нового клиента.

    - Для добавления методом POST передается json {"start_send":, "end_send":, "text":, "filter_client"}

    - Для удаления методом DELETE передается json {"id_delete":}


 - api/mailing/<id_update> - обновление данных клиента с id=<id_update>

    - Для обновления методом PUT передается json {"up_start_send":, "up_end_send":, "up_text":, "up_filter_client"}

---
###Запуск рассылки.
 - api/mailing/start/<id_mailing>' - запускает рассылку с id=<id_mailing>

---

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

