# BooksStore - Онлайн магазин книг

## Описание проекта
BooksStore - это веб-приложение для онлайн-магазина книг, разработанное с использованием Django. Проект предоставляет удобный интерфейс для покупки книг, управления корзиной и отслеживания заказов.

## Основной функционал

### Для пользователей
- Регистрация и авторизация
- Личный кабинет с возможностью редактирования профиля
- Просмотр каталога книг
- Добавление книг в корзину
- Управление корзиной (добавление/удаление товаров)
- Оформление заказов
- Просмотр истории заказов

### Для администраторов
- Доступ к панели администратора Django
- Управление каталогом книг (добавление, редактирование, удаление)
- Управление пользователями
- Просмотр и управление заказами

## Технологии
- Python 3.8.2
- Django 4.2.20
- Bootstrap 5
- AJAX для асинхронных запросов
- MySQL для хранения данных

## Предварительные требования
- Python 3.8.2 или выше
- MySQL Server
- pip (менеджер пакетов Python)

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd web-AI-prog-p1
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте базу данных MySQL:
   - Создайте базу данных:
   ```sql
   CREATE DATABASE bookstore;
   ```
   - Убедитесь, что у вас есть доступ к MySQL с указанными в `settings.py` учетными данными:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'bookstore',
             'USER': 'root',
             'PASSWORD': '2005037',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```
   - При необходимости измените настройки подключения к базе данных в `echoserver/settings.py`

5. Перейдите в директорию проекта:
```bash
cd echoserver
```

6. Примените миграции:
```bash
python manage.py migrate
```

7. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

8. Запустите сервер:
```bash
python manage.py runserver
```

## Структура проекта
```
echoserver/
├── echoapp/
│   ├── migrations/
│   ├── templates/
│   │   └── echoapp/
│   │       ├── base.html          # Базовый шаблон
│   │       ├── profile.html       # Страница профиля
│   │       ├── cart.html         # Корзина
│   │       ├── orders.html       # История заказов
│   │       ├── book_list.html    # Список книг
│   │       └── bookstore.html    # Главная страница магазина
│   ├── models.py                 # Модели данных
│   ├── views.py                 # Представления
│   ├── forms.py                 # Формы
│   └── urls.py                  # URL маршруты
├── echoserver/
│   ├── settings.py              # Настройки проекта
│   ├── urls.py                 # Корневые URL
│   └── wsgi.py                 # WSGI конфигурация
└── manage.py
```

## Основные модели

### User
- Расширенная модель пользователя с дополнительным полем role
- Поддержка ролей: пользователь (user) и администратор (admin)
- Наследует стандартные поля Django AbstractUser

### Book
- Информация о книгах
- Поля: 
  - title (название, CharField)
  - author (автор, CharField)
  - price (цена, DecimalField)

### Cart
- Корзина пользователя
- Поля:
  - user (OneToOneField к User)
  - items (JSONField для хранения товаров)
- Методы для работы с товарами (get_items, set_items)

### Order
- Заказы пользователей
- Поля:
  - user (ForeignKey к User)
  - created_at (дата создания)
  - items (JSONField для хранения состава заказа)
  - total_price (общая стоимость)
- Сортировка по дате создания (от новых к старым)

## Доступ к системе

После запуска проект будет доступен по адресу: http://127.0.0.1:8000/

- Панель администратора: http://127.0.0.1:8000/admin/
- Каталог книг: http://127.0.0.1:8000/
- Личный кабинет: http://127.0.0.1:8000/profile/
- Корзина: http://127.0.0.1:8000/cart/
- История заказов: http://127.0.0.1:8000/orders/
