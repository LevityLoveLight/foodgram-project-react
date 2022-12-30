# Проект "Foodgram"

![example workflow](https://github.com/LevityLoveLight/foodgram-project-react/actions/workflows/main.yml/badge.svg)  
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

Онлайн-сервис «Foodgram» - продуктовый помощник, который позволяет пользователям публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Как запустить проект

### Подготовка сервера для развертывания 

- Установить Docker и Docker Compose на сервер:
```
 sudo apt-get update
 sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
 ```

 - Скопировать файлы `docker-compose.yml` и `nginx.conf` из директории `infra` на сервер:
 ```
 scp infra/docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
 scp infra/nginx.conf <username>@<host>:/home/<username>/nginx.conf
 ```

- Создать файл .env и указать в нем переменные окружения:
```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
DJANGO_SECRET_KEY=<секретный ключ Django>
HOST=<IP-адрес сервера>
```

- В конфигурационном файле nginx.conf в строке server_name указать IP-адрес сервера:
```
Пример: server_name localhost;
```

### Настройка Github Actions для автоматического деплоя

В файле .github/workflows/main.yml описан Workflow для автоматической сборки проекта и развертывания на сервере. 

Workflow состоит из трех шагов:

- Проверка кода на соответствие PEP8
- Сборка и публикация образа бэкенда на DockerHub.
- Автоматический деплой на удаленный сервер.

Для работы с Workflow нужно добавить в GitHub Secrets переменные окружения для работы:

```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>

DOCKER_USERNAME=<имя пользователя>
DOCKER_PASSWORD=<пароль от DockerHub>

DJANGO_SECRET_KEY=<секретный ключ проекта Django> (нельзя использовать знак & в ключе)

USER=<username для подключения к серверу>
HOST=<IP сервера>
SSH_KEY=<приватный SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>
PASSPHRASE=<пароль для SSH-ключа, если он установлен>
```

### Развертывание проекта на сервере

- Собрать проект на сервере:
```
sudo docker compose up -d --build
```

- Применить миграции:
```
sudo docker compose exec backend python manage.py migrate
```

- Собрать статичные файлы:
```
sudo docker compose exec backend python manage.py collectstatic
```

- Загрузить ингридиенты в базу данных:
```
sudo docker compose exec backend python manage.py load_ingredients
```
- Загрузить тэги в базу данных:
```
sudo docker compose exec backend python manage.py load_tags
```

- Создать суперпользователя Django:
```
sudo docker compose exec backend python manage.py createsuperuser
```
