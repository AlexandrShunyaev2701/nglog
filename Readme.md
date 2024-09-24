# Nginx Log Parser Django Application

## Описание проекта

Это Django-приложение для обработки и агрегации Nginx логов. 
Приложение включает Management command для парсинга логов с удаленной ссылки и сохранения их в базу данных. 
Также реализован API (на базе Django Rest Framework) и админка для отображения загруженных данных.

### Возможности приложения:
- Парсинг Nginx логов с удаленного URL в формате JSON и сохранение данных в базу данных.
- Django Admin для просмотра, фильтрации и поиска по загруженным данным.
- REST API для доступа к данным с поддержкой пагинации, фильтрации и поиска.
- Swagger документация для API.
- Упаковка проекта в Docker и Docker Compose для упрощенного развёртывания.

## Установка и запуск проекта
### 1. Клонирование репозитория

```bash
git clone ...
cd <папка с проектом>
```
### 2. Настройка виртуальной среды
```bash
python -m venv .venv
source .venv/bin/activate
```
### 3. Конфигурация переменных окружения
Создайте файл .env по примеру .env.example

### 4. Запуск проекта с помощью Docker
```bash
docker-compose up --build
```

### 5. Миграции базы данных
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 6. Парсинг логов
Выполните вход в контейнер с приложением Django и выполните комманду, так же передайте туда ссылку на логи по примеру:
```bash
docker-compose exec web python manage.py parser_logs 'https://drive.google.com/file/d/18Ss9afYL8xTeyVd0ZTfFX9dqja4pBGVp/view?usp=sharin]'
```

## Работа с API

API разработан на базе Django Rest Framework и доступен по следующим маршрутам:

	/nginx_log/ - список всех логов (GET, POST).
	/nginx_log/logs/ - список всех логов с возможностью фильтрации
    (фильтрация по: 'request_date', 'http_method', 'response_code),
    поиска (поиск по 'ip_address', 'uri', 'user_agent).
	Пагинация: по умолчанию возвращает 10 записей на страницу.

Документация API доступна по адресу:

	Swagger UI: http://localhost:8000/swagger/
	ReDoc: http://localhost:8000/redoc/
