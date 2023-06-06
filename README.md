# YaMDb API: CI и CD проекта
## Описание проекта

Проект для публикаций отзывов пользователей на произведения. 
Читатели оставляют к произведениям текстовые отзывы и выставляют рейтинг.
Полная документация к API находится по эндпоинту: /redoc
```      
⚠️ Проект идет исключительно как API, фронта нет
```

## Технологии
<img src="https://img.shields.io/badge/Python%203.7-grey?style=for-the-badge&logo=Python&logoColor=Blue"><img src="https://img.shields.io/badge/Django%203.2-grey?style=for-the-badge&logo=Django&logoColor=darkgreen"><img src="https://img.shields.io/badge/DRF%203.12.4-grey?style=for-the-badge&logo=Django&logoColor=white"><img src="https://img.shields.io/badge/Gunicorn%2020.0.4-grey?style=for-the-badge&logo=Gunicorn&logoColor=green"><img src="https://img.shields.io/badge/Nginx%201.21.3-grey?style=for-the-badge&logo=Nginx&logoColor=black"><img src="https://img.shields.io/badge/PostgreSQL%2013.0-grey?style=for-the-badge&logo=PostgreSQL&logoColor=Blue"><img src="https://img.shields.io/badge/Docker%2020.10.23-grey?style=for-the-badge&logo=Docker&logoColor=Blue"><img src="https://img.shields.io/badge/Docker Compose%202.15.1-grey?style=for-the-badge&logo=Docker&logoColor=Blue">


## Подготовка проекта

1. 🔽 Клонируйте репозиторий:
```      
git clone https://github.com/Jenkneo/yamdb_final
```
2. 👨🏻‍💻 Настройте удаленный сервер:
```
# Создайте в домашней директории папку nginx
mkdir nginx

#Установите Docker и Docker-compose
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
3. ✏️ Отредактируйте docker-compose.yaml (15 строка):
```
image: <ваш-dockerhub>/yamdb_final:latest
```
4. ☁ Отправьте необходимые данные на сервер:
```
# Скопируйте docker-compose.yaml в домашнюю директорию сервера
scp -rv C:\<путь_до_файла>\docker-compose.yaml <ваш_username>@<ip_сервера>:/home

# Скопируйте default.conf в созданную папку nginx
scp -rv C:\<путь_до_файла>\nginx\default.conf <ваш_username>@<ip_сервера>:/home/nginx
```
5. ⚙️ В репозитории на github добавьте secret данные. `Settings - Secrets and variables - Actions`:
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
1. 🔼 Запушьте свой проект на github:
```
git push
```
2. ⌛ Немного подождите когда проект задеплоится на сервер.
3. ✅ Проверьте работоспособность проекта перейдя по адресу сервера в браузере.
```
http://<server_ip>/redoc
```
## Донастройка проекта
1. 🔗 Подключитесь по ssh и соберите статистические файлы:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
2. ⚙️ Примените миграции.
```
sudo docker-compose exec web python manage.py makemigrations reviews
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate --noinput
```
3. ⚙️ Создайте суперпользователя.
```
sudo docker-compose exec web python manage.py createsuperuser
```

### Разработчики:

- [Алексей](https://github.com/alekseikogan)
- [Евгений](https://github.com/Jenkneo)
- [Екатерина](https://github.com/katiefrompiter)

### Идея проекта - [Яндекс Практикум](https://practicum.yandex.ru/) 


