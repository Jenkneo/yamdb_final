![example workflow](https://github.com/jenkneo/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Проект 16 спринта: CI и CD проекта api_yamdb
## Описание проекта

Проект для публикаций отзывов пользователей на произведения.

Читатели оставляют к произведениям текстовые отзывы и выставляют рейтинг.

Полная документация к API находится по эндпоинту: /redoc


## Подготовка проекта

1. Клонируйте репозиторий:
```      
git clone https://github.com/Jenkneo/yamdb_final
```
2. Настройте удаленный сервер:
```
# Создайте в домашней директории папку nginx
mkdir nginx

#Установите Docker и Docker-compose
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
3. Отправьте необходимые данные на сервер:
```
# Скопируйте docker-compose.yaml в домашнюю директорию сервера
scp -rv C:\<путь_до_файла>\docker-compose.yaml <ваш_username>@<ip_сервера>:/home

# Скопируйте default.conf в созданную папку nginx
scp -rv C:\<путь_до_файла>\nginx\default.conf <ваш_username>@<ip_сервера>:/home/nginx
```
4. В репозитории на github добавьте secret данные. `Settings - Secrets and variables - Actions`:
```
DB_NAME - Имя базы данных (Например - postgres)
DB_USER - Имя пользователя базы данных (Например - postgres)
DB_PASSWORD - Пароль пользователя базы данных (Например - postgres)

DOCKER_USERNAME - Логин от DockerHub
DOCKER_PASSWORD - Пароль от DockerHub

EMAIL_HOST - Хост сервера почты (Пример - smtp.gmail.com) 
EMAIL_PORT - Порт сервера почты (Пример - 587) 
EMAIL_HOST_USER - Почта сервера (Пример - server_mail@gmail.com) 
EMAIL_HOST_PASSWORD - Пароль почтового ящика

SSH_HOST - IP адрес вашего удаленного сервера
SSH_KEY - id_rsa закрытого ключа для подключения к серверу
SSH_USER - логин на удаленном сервере

TELEGRAM_TOKEN - токен бота полученный от @BotFather
TELEGRAM_TO - id вашего Telegram аккаунта
```

## Запуск проекта
1. Запушьте свой проект на github:
```
git push
```
2. Немного подождите когда проект задеплоится на сервер.
3. Проверьте работоспособность проекта перейдя по адресу сервера в браузере.
```
http://<server_ip>/admin
```
## Донастройка проекта
1. Подключитесь по ssh и соберите статистические файлы:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
2. Примените миграции.
```
sudo docker-compose exec web python manage.py makemigrations reviews
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate --noinput
```
3. Создайте суперпользователя.
```
sudo docker-compose exec web python manage.py createsuperuser
```

## Технологии
### Python
- Python 3.7-slim
- Django 3.2
- Django Rest Framework 3.12.4
- Gunicorn 20.0.4

### Сервер
- Nginx 1.21.3

### База данных
- PostgreSQL 13.0

### Контейнер
- Docker 20.10.23
- Docker Compose 2.15.1

## О проекте
Идея проекта - [Яндекс Практикум](https://practicum.yandex.ru/) 

### Разработчики:
- [Алексей](https://github.com/alekseikogan)
- [Евгений](https://github.com/Jenkneo)
- [Екатерина](https://github.com/katiefrompiter)

## Адрес тестового проекта
[Yandex Cloud](http://158.160.14.36/redoc/) 
