# Проект GRPC с Alembic и gRPC

## Установка и настройка

1. Создайте виртуальное окружение:

```bash
python3 -m venv venv
```

2. Активируйте виртуальное окружение:

```bash
source venv/bin/activate
```

3. установка зависимостей
```
pip install -r requirements.txt
```


4. генерация grpc кода
```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. reporting.proto
```

Проект состоит из сервера и клиента

Килент общий для трех частей. Запустите его чтобы он мог отправлять сообщения со структурой кораблей
```
python3 src/reporting_server.py
```

## Part 1
### Получение корабля в json-стиле от GRPC сервера

```
python3 src/reporting_client.py 17 45 40.0409 -29 00 28.118
```

## Part 2
### Валидация кораблей с помощью pydantic

Рекомендуем увеличить количество посылаемых кораблей в сервере

```
python3 src/reporting_client_v2.py 17 45 40.0409 -29 00 28.118
```

## Part 3

### Сохранение в базу данных

Настройки подключения базы данных хранятся в .env в корне проекта
```
python3 src/reporting_client_v3.py scan 17 45 40.0409 -29 00 28.118 
```
### Поиск "Предателей"
```
python3 src/reporting_client_v3.py list-traitors
```

## Bonus part

Не забудьте указать настройки подключения к базе данных в файле

alembic.ini

Вы можете посмотреть историю миграции
```bash
alembic history 
```

Посмотреть текущую версию
```bash
alembic current
```

Создать новую миграцию
```bash
alembic revision --autogenerate -m "new migration"
```

Применить новую миграцию
```bash
alembic upgrade head
```