# 📧 Система управления рассылками (Mailing List Service)

![Django](https://img.shields.io/badge/Django-5.0-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Poetry](https://img.shields.io/badge/Poetry-1.7+-orange)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.2-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

Веб-приложение на Django для управления email рассылками с продвинутой системой ролей, аутентификацией и детальной статистикой.

## 🎯 Основные возможности

### 👤 Для пользователей
- ✅ **Управление клиентами** - CRUD операции для получателей рассылок
- ✅ **Создание сообщений** - шаблоны писем с предпросмотром
- ✅ **Управление рассылками** - планирование и отправка email кампаний
- ✅ **Личный кабинет** - редактирование профиля с аватаром
- ✅ **Статистика** - просмотр результатов отправки в реальном времени
- ✅ **Подтверждение email** - обязательная верификация при регистрации

### 👨‍💼 Для менеджеров
- ✅ **Просмотр всех данных** - полный доступ к пользователям, клиентам и рассылкам
- ✅ **Управление пользователями** - блокировка/разблокировка аккаунтов
- ✅ **Контроль рассылок** - отключение активных email кампаний
- ✅ **Дашборд** - общая статистика по системе
- ✅ **Изменение ролей** - назначение прав доступа пользователям

### 🛡 Система безопасности
- ✅ **Трехуровневая ролевая модель** (Пользователь/Менеджер/Администратор)
- ✅ **Подтверждение email** при регистрации
- ✅ **Восстановление пароля** через email
- ✅ **Защита от CSRF и XSS** атак
- ✅ **Валидация входных данных** на всех формах
- ✅ **Ограничение доступа** к чужим данным

## 🛠 Технологический стек

### Backend
- **Django 5.x** - основной фреймворк
- **Django ORM** - работа с базой данных
- **Django Templates** - система шаблонов
- **Django Auth** - система аутентификации (расширенная)

### Frontend
- **Bootstrap 5** - адаптивный дизайн
- **Font Awesome** - иконки
- **JavaScript** - интерактивные элементы
- **CSS3** - кастомные стили

### Инфраструктура
- **Poetry** - менеджер зависимостей
- **SQLite/PostgreSQL** - базы данных
- **SMTP** - отправка email
- **Docker** (готово к контейнеризации)

## 📦 Установка и запуск

### Предварительные требования

- **Python 3.11** или выше
- **Poetry** 1.7.0 или выше
- **Git** для клонирования репозитория

### Шаг 1: Установка Poetry

```bash
# Установка через официальный скрипт (рекомендуется)
curl -sSL https://install.python-poetry.org | python3 -

# Или через pip
pip install poetry

# Проверка установки
poetry --version
```

### Шаг 2: Клонирование и настройка проекта

```bash
# Клонирование репозитория
git clone <repository-url>
cd mailing_list_service

# Установка зависимостей через Poetry
poetry install

# Активация виртуального окружения
poetry shell
```

### Шаг 3: Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
# ========================
# Базовые настройки Django
# ========================
SECRET_KEY=django-insecure-your-secret-key-here-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ========================
# Настройки базы данных
# ========================

# Вариант 1: SQLite (рекомендуется для разработки)
DATABASE_URL=sqlite:///db.sqlite3

# Вариант 2: PostgreSQL (для продакшена)
# DATABASE_URL=postgresql://username:password@localhost:5432/mailing_db

# ========================
# Настройки Email (SMTP)
# ========================
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend  # Для разработки

# Для продакшена раскомментируйте:
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.yandex.ru
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@yandex.ru
# EMAIL_HOST_PASSWORD=your-app-password
# DEFAULT_FROM_EMAIL=your-email@yandex.ru

# ========================
# Медиа файлы
# ========================
MEDIA_URL=/media/
MEDIA_ROOT=media/
```

### Шаг 4: Настройка базы данных и создание суперпользователя

```bash
# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Сбор статических файлов
python manage.py collectstatic --noinput
```

### Шаг 5: Запуск сервера разработки

```bash
# Запуск сервера
python manage.py runserver
```

Приложение будет доступно по адресам:
- **Основное приложение**: http://127.0.0.1:8000
- **Административная панель**: http://127.0.0.1:8000/admin
- **Документация API**: http://127.0.0.1:8000/api/docs/ (если включен DRF)

## 🏗 Структура проекта

```
mailing_list_service/
├── pyproject.toml              # Конфигурация Poetry и зависимостей
├── manage.py                   # Точка входа Django
├── .env.example               # Пример переменных окружения
├── .gitignore                 # Игнорируемые файлы Git
├── README.md                  # Документация
│
├── config/                    # Основные настройки проекта
│   ├── __init__.py
│   ├── settings.py           # Настройки Django
│   ├── urls.py               # Корневые URL маршруты
│   └── wsgi.py               # WSGI конфигурация
│
├── mailing/                   # Основное приложение рассылок
│   ├── __init__.py
│   ├── admin.py              # Админка для моделей рассылок
│   ├── apps.py
│   ├── models.py             # Модели: Клиент, Сообщение, Рассылка, Попытка
│   ├── views.py              # CBV представления для CRUD операций
│   ├── forms.py              # Формы для моделей
│   ├── services.py           # Сервисы отправки email
│   ├── mixins.py             # Миксины для проверки прав доступа
│   ├── urls.py               # URL маршруты приложения
│   ├── management/           # Кастомные команды
│   │   └── commands/
│   │       └── send_mailing.py
│   ├── templatetags/         # Кастомные теги шаблонов
│   │   ├── __init__.py
│   │   └── mailing_extras.py
│   └── templates/            # Шаблоны приложения
│       └── mailing/
│           ├── base.html
│           ├── home.html
│           ├── client_*.html
│           ├── message_*.html
│           └── mailing_*.html
│
├── users/                    # Приложение пользователей
│   ├── __init__.py
│   ├── admin.py             # Админка для пользователей
│   ├── apps.py
│   ├── models.py            # Кастомная модель User + UserProfile
│   ├── views.py             # Аутентификация и профиль
│   ├── views_manager.py     # Представления для менеджеров
│   ├── forms.py             # Формы аутентификации
│   ├── mixins.py            # Миксины для проверки ролей
│   ├── urls.py              # URL маршруты пользователей
│   └── templates/           # Шаблоны аутентификации
│       └── users/
│           ├── login.html
│           ├── register.html
│           ├── profile.html
│           ├── profile_edit.html
│           └── password_*.html
│
├── static/                  # Статические файлы (CSS, JS, изображения)
│   ├── css/
│   ├── js/
│   └── images/
│
└── media/                   # Медиа файлы (загружаемые пользователями)
    └── user/avatar/
```

## 🗄 Модели данных

### 👤 User (Кастомная модель)
- `email` - уникальный идентификатор (вместо username)
- `role` - роль (user/manager/admin)
- `is_blocked` - статус блокировки
- `email_verified` - подтверждение email
- `verification_token` - токен для подтверждения

### 👥 UserProfile
- `avatar` - аватар пользователя
- `phone_number` - номер телефона
- `country` - страна
- `company` - компания

### 📇 Client
- `email` - email клиента (уникальный)
- `full_name` - Ф.И.О. клиента
- `comment` - комментарий
- `owner` - владелец (связь с User)

### 📝 Message
- `subject` - тема письма
- `body` - тело письма
- `owner` - владелец

### 📧 Mailing
- `start_time` - время начала рассылки
- `end_time` - время окончания
- `status` - статус (created/started/completed)
- `message` - шаблон сообщения
- `clients` - список получателей
- `owner` - владелец

### 📊 MailingAttempt
- `attempt_time` - время попытки отправки
- `status` - результат (success/failed)
- `server_response` - ответ почтового сервера
- `mailing` - связанная рассылка

## 🔐 Система ролей и прав доступа

### Уровни доступа:

#### 👤 Пользователь (User)
```yaml
Разрешено:
  - Создание/редактирование/удаление своих клиентов
  - Создание/редактирование/удаление своих сообщений
  - Создание/редактирование/удаление своих рассылок
  - Отправка своих рассылок (ручная и тестовая)
  - Просмотр статистики по своим рассылкам
  - Редактирование своего профиля

Запрещено:
  - Доступ к данным других пользователей
  - Просмотр системной статистики
  - Управление пользователями
```

#### 👨‍💼 Менеджер (Manager)
```yaml
Все права пользователя, плюс:
  - Просмотр всех пользователей системы
  - Просмотр всех клиентов
  - Просмотр всех сообщений
  - Просмотр всех рассылок
  - Блокировка/разблокировка пользователей
  - Отключение активных рассылок
  - Доступ к дашборду системы
```

#### 👑 Администратор (Admin)
```yaml
Все права менеджера, плюс:
  - Изменение ролей пользователей
  - Полный доступ к админ-панели Django
  - Управление всеми настройками системы
```

## 📊 API и команды

### Консольные команды

```bash
# Отправка рассылки по ID
python manage.py send_mailing <mailing_id>

# Создание тестовых данных
python manage.py create_test_data

# Проверка статусов рассылок
python manage.py check_mailing_status
```

### Email сервисы

```python
# Пример использования сервиса отправки
from mailing.services import EmailService
from mailing.models import Mailing

mailing = Mailing.objects.get(pk=1)
successful, failed = EmailService.send_mailing_bulk(mailing)
```

## 🎨 Интерфейс

### Ключевые страницы

#### Главная страница (`/`)
- Статистика системы
- Быстрый доступ к основным разделам
- Информация об активных рассылках

#### Управление клиентами (`/clients/`)
- Таблица всех клиентов
- Поиск и фильтрация
- Массовые операции
- Экспорт данных

#### Создание рассылки (`/mailings/create/`)
- Выбор шаблона сообщения
- Выбор получателей
- Настройка времени отправки
- Предпросмотр письма

#### Панель управления (`/users/manager/dashboard/`)
- Общая статистика системы
- Активность пользователей
- Мониторинг рассылок
- Быстрые действия

## 🔧 Настройка для продакшена

### 1. Настройка базы данных PostgreSQL

```env
# .env.production
DATABASE_URL=postgresql://username:password@host:5432/dbname
```

### 2. Настройка SMTP сервера

```env
# .env.production
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@yandex.ru
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@yandex.ru
```

### 3. Настройки безопасности

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```


```

## 📈 Мониторинг и логирование

### Настройка логирования

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
        'mailing_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/mailing.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'mailing': {
            'handlers': ['mailing_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

## 🚀 Быстрый старт

```bash
# Клонирование
git clone https://github.com/yourusername/mailing-list-service.git
cd mailing-list-service

# Настройка Poetry
poetry install
poetry shell

# Настройка окружения
cp .env.example .env
# Отредактируйте .env файл

# Миграции и суперпользователь
python manage.py migrate
python manage.py createsuperuser

# Запуск
python manage.py runserver
```

## 🤝 Вклад в проект

Мы приветствуем вклад в проект! Пожалуйста, следуйте этим шагам:

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add some amazing feature'`)
4. Запушьте ветку (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

### Стандарты кода

```bash
# Проверка форматирования кода
poetry run black .

# Проверка стиля кода
poetry run flake8

# Проверка импортов
poetry run isort .
```

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

## 📞 Поддержка и контакты

- **Issues**: [GitHub Issues](https://github.com/yourusername/mailing-list-service/issues)
- **Email**: rodionmarochkin32@gmail.com
- **Документация**: [Документация проекта](docs/)

## 🙏 Благодарности

- Команде Django за отличный фреймворк
- Сообществу Bootstrap за прекрасный UI инструментарий
- Всем контрибьюторам проекта

---

**Разработано с ❤️ для эффективного управления email рассылками**

*Последнее обновление: Декабрь 2025*