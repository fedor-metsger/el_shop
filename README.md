
# Проект «API сервиса заказа товаров для розничных сетей»

Проект выполнен в рамках дипломной работы к профессии **«Python-разработчик»**

## Оглавление
[Описание](#Описание)  
[Интерфейс](#интерфейс)  
[Архитектура и используемый стек](#архитектура-и-используемый-стек)  
[Путеводитель по коду](#путеводитель-по-коду)  
[Docker и Docker Compose](#docker-и-docker-compose)  


## Описание
Результатом проекта является набор модулей на языке python, которые позволяют:
1. Продавцам регистрировать свой магазин и размещать список товаров с описанием и ценами.
1. Покупателям выбирать товары из списков и создавать заказ,
а так же назначать заказ на определённый адрес (контакт).


## Интерфейс
Интерфейсом программы является API, выполненная с использованием технологии REST.
Далее приводится описание используемых URL и методов:

### Ресурс /api/v1/user/login/
- Метод **GET** - служит для получения JWT токена. Формат запроса:
```json
{
   "email": "svyaznoy@yandex.ru",
   "password": "pasword"
}
```
Ответ:
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5OTI2ODUwMiwiaWF0IjoxNjk5MTgyMTAyLCJqdGkiOiI1MTk1OGI4YjFkMTQ0NWY5ODBjODQ3NjNkZmE2OTcyNCIsInVzZXJfaWQiOjF9.GnRhWesO4ih24fr9bWApWPUeYwfsY98b0Ndj9dce2cE",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk5MjE4MTAyLCJpYXQiOjE2OTkxODIxMDIsImp0aSI6IjRkNmRkZGJmNGJhMjRiYjE5ZjgwYzY3NTdkNTAwODY1IiwidXNlcl9pZCI6MX0.hqIgduh8pcmscsukx9l_cm1E1vPUr5k_P7sMJvoT8OM"
}
```
Ответ при неправильных данных запроса:
```json
{
    "detail": "No active account found with the given credentials"
}
```

### Ресурс /api/v1/user/register/
- Метод **POST** - служит для регистрации нового пользователя. Формат запроса:
```json
{
   "username": "dad",
   "password": "password",
   "email": "user2@yandex.ru",
   "company": "",
   "position": "",
   "type": "customer"
}
```
Ответ:
```json
{
    "username": "dad",
    "email": "user2@yandex.ru",
    "password": "password",
    "company": "",
    "position": "",
    "type": "customer"
}
```
Пример ответа при неправильных данных запроса:
```json
{
    "username": [
        "Пользователь с таким именем уже существует."
    ],
    "email": [
        "This field may not be blank."
    ]
}
```
### Ресурс /api/v1/user/contact/
- Метод **GET** - служит для получения всех контактов пользователя. Формат запроса:

Ответ:
```json
[
    {
        "id": 1,
        "city": "Санкт-Петербург",
        "street": "Советская",
        "house": "12",
        "structure": "2",
        "building": "",
        "apartment": "35",
        "phone": "+78123457823"
    }
]
```
- Метод **GET** - служит для получения всех пользователя. Формат запроса:
Ответ:
```json
[
    {
        "id": 1,
        "city": "Санкт-Петербург",
        "street": "Советская",
        "house": "12",
        "structure": "2",
        "building": "",
        "apartment": "35",
        "phone": "+78123457823"
    }
]
```
- Метод **POST** - служит для создания нового контакта пользователя:
```json
    {
        "city": "Санкт-Петербург",
        "street": "Советская",
        "house": "12",
        "structure": "2",
        "building": "",
        "apartment": "35",
        "phone": "+78123457823"
    }
```
Ответ:
```json
{
    "Status": true
}
```
Пример ответа при неправильных данных запроса:
```json
{
    "Status": false,
    "Errors": {
        "street": [
            "This field may not be blank."
        ]
    }
}
```
- Метод **DELETE** - служит для удаления контакта пользователя:
```json
{
    "items": "1,2"
}
```
Ответ:
```json
{
    "Status": true,
    "Удалено объектов": 2
}
```
Пример ответа при неправильных данных запроса:
```json
{
    "Status": true,
    "Удалено объектов": 0
}
```
### Ресурс /api/v1/partner/update/
- Метод **POST** - служит для загрузки прайс-листа от магазина. Формат запроса:
```json
{
   "url": "https://raw.githubusercontent.com/fedor-metsger/el_shop/main/svyaznoy.yaml"
}
```
Ответ. Возвращается идентификатор задачи **Celery**:
```json
{
    "status": true,
    "task_id": "bb71ea8c-9a25-4b6f-9bf6-10929336a51c"
}
```
Пример ответа при неправильных данных запроса:
```json
{
    "Status": false,
    "Errors": "Не указаны все необходимые аргументы"
}
``` 
### Ресурс /api/v1/partner/update/<str:id>/>
- Метод **GET** - служит для проверки состояния фоновой задачи загрузки прайс-листа.
  В параметр **id** нужно передать полученный ранее **id** задачи **Celery**.
Ответ:
```json
{
    "task_id": "c20a1df8-b4a2-44f8-a205-e881715145e8",
    "task_info": "None"
}
```
Пример ответа при неправильных данных запроса:
```json
{
    "task_id": "9d42b1ca-c63a-44a0-87f8-85ecf82708c4",
    "task_info": "value too long for type character varying(80)\n"
}
``` 
### Ресурс /api/v1/categories/>
- Метод **GET** - служит для списка загруженных категорий товаров.
Ответ:
```json
[
    {
        "id": 224,
        "name": "Смартфоны"
    },
    {
        "id": 15,
        "name": "Аксессуары"
    },
    {
        "id": 1,
        "name": "Flash-накопители"
    }
]
```
### Ресурс /api/v1/shops/>
- Метод **GET** - служит для списка загруженных магазинов.
Ответ:
```json
[
    {
        "id": 1,
        "name": "Связной",
        "state": true
    },
    {
        "id": 2,
        "name": "Евросеть",
        "state": true
    },
    {
        "id": 3,
        "name": "DNS",
        "state": true
    }
]
```
### Ресурс /api/v1/shops/>
- Метод **GET** - служит для списка загруженных магазинов.
Ответ:
```json
[
    {
        "id": 1,
        "name": "Связной",
        "state": true
    },
    {
        "id": 2,
        "name": "Евросеть",
        "state": true
    },
    {
        "id": 3,
        "name": "DNS",
        "state": true
    }
]
```
### Ресурс /api/v1/products/>
- Метод **GET** - служит для списка загруженных магазинов.
Ответ:
```json
[
    {
        "id": 5,
        "model": "apple/iphone/xs-max",
        "product": {
            "name": "Смартфон Apple iPhone XS Max 512GB (золотистый)",
            "category": "Смартфоны"
        },
        "shop": {
            "id": 2,
            "name": "Евросеть",
            "state": true
        },
        "quantity": 24,
        "price": 108000,
        "price_rrc": 116990,
        "product_parameters": [
            {
                "parameter": "Диагональ (дюйм)",
                "value": "6.5"
            },
            {
                "parameter": "Разрешение (пикс)",
                "value": "2688x1242"
            },
            {
                "parameter": "Встроенная память (Гб)",
                "value": "512"
            },
            {
                "parameter": "Цвет",
                "value": "серый"
            }
        ]
    }
]
```
### Ресурс /api/v1/basket/
- Метод **POST** - служит для внесения покупателем товаров в корзину.
```json
[
   {"product_info": 6, "quantity": 1},
   {"product_info": 7, "quantity": 1},
   {"product_info": 8, "quantity": 1}
]
```
Ответ:
```json
{
   "Status": true,
   "Создано объектов": 3
}
```
### Ресурс /api/v1/order/
- Метод **GET** - служит для получения списка заказов покупателем.
```json
[
    {
        "id": 29,
        "state": "new",
        "dt": "2023-11-05T13:40:49.427277Z",
        "count_items": 3,
        "total_sum": 5600
    }
]
```
- Метод **POST** - служит для создания контакта покупателем.
```json
{
    "contact": 6
}
```
Ответ:
```json
{
    "Status": true
}
```
Пример ответа при неправильных данных запроса:
```json
{
    "Status": false,
    "Error": "Корзина пуста"
}
```
### Ресурс /api/v1/order/<int:id>
- Метод **GET** - служит для получения информации по одному заказу
Ответ:
```json
{
    "id": 29,
    "ordered_items": [
        {
            "id": 44,
            "product_info": {
                "id": 6,
                "model": "trascend/1gb",
                "product": {
                    "name": "USB drive Trascend 1Gb",
                    "category": "Flash-накопители"
                },
                "shop": {
                    "id": 2,
                    "name": "Евросеть",
                    "state": true
                },
                "quantity": 39,
                "price": 1000,
                "price_rrc": 900,
                "product_parameters": [
                    {
                        "parameter": "Ёмкость (Мб)",
                        "value": "1000"
                    },
                    {
                        "parameter": "Цвет",
                        "value": "красный"
                    }
                ]
            },
            "quantity": 1
        },
        {
            "id": 45,
            "product_info": {
                "id": 7,
                "model": "trascend/2gb",
                "product": {
                    "name": "USB drive Trascend 2Gb",
                    "category": "Flash-накопители"
                },
                "shop": {
                    "id": 2,
                    "name": "Евросеть",
                    "state": true
                },
                "quantity": 25,
                "price": 1600,
                "price_rrc": 1500,
                "product_parameters": [
                    {
                        "parameter": "Ёмкость (Мб)",
                        "value": "2000"
                    },
                    {
                        "parameter": "Цвет",
                        "value": "черный"
                    }
                ]
            },
            "quantity": 1
        },
        {
            "id": 46,
            "product_info": {
                "id": 8,
                "model": "trascend/4gb",
                "product": {
                    "name": "USB drive Trascend 4Gb",
                    "category": "Flash-накопители"
                },
                "shop": {
                    "id": 2,
                    "name": "Евросеть",
                    "state": true
                },
                "quantity": 12,
                "price": 3000,
                "price_rrc": 2900,
                "product_parameters": [
                    {
                        "parameter": "Ёмкость (Мб)",
                        "value": "4000"
                    },
                    {
                        "parameter": "Цвет",
                        "value": "черный"
                    }
                ]
            },
            "quantity": 1
        }
    ],
    "state": "new",
    "dt": "2023-11-05T13:40:49.427277Z",
    "contact": {
        "id": 7,
        "city": "Москва",
        "street": "Милашенкова",
        "house": "12",
        "structure": "2",
        "building": "",
        "apartment": "138",
        "phone": "+79262001121"
    }
}
```
Пример ответа при неправильных данных запроса:
```json
{
    "detail": "You do not have permission to perform this action."
}
```
## Архитектура и используемый стек
Для реализации поставленной задачи было выбрано следующее решение:
1. Реляционная БД для хранения загруженной информации. Реляционная БД была выбрана потому,
   что характер хранимых данных соответствует сущностям разных типов со связями **"один ко многим"**
   и **"многие ко многим"**. В качестве конкретной СУБД была выбрана **PostgreSQL**.
1. Процедура создания БД и интерфейс администратора были реализованы с помощью фреймворка **Django**,
   как наиболее полно отвечающему требованиям задачи:
   - Создание БД и первоначальная миграция;
   - удобный интерфейс для администрирования БД;
   - Возможность запуска задач в фоне.
1. Для реализации принципов подхода REST используется пакет **djangorestframework**.
1. Для упрощения идентификации и авторизации пользователей используется
   пакет **djangorestframework-simplejwt**.  
1. Для запуска задач в фоне используется пакет **celery**.
   Выбор данного пакета обусловлен наличием требуемого функционала а так же хорошей
   документированностью и простостотой в использовании.
1. В качестве брокера сообщений для **celery** используется ПО **REDIS**
   и соответствующий ему python-пакет **redis**.

## Путеводитель по коду
### Backend
Для реализации доступа к БД разработан пакет [backend](backend).

В нём реализованы следующие модели:

1. [User](https://github.com/fedor-metsger/el_shop/blob/a9bc5bf27d0dda60960f046876c2649292acf31d/backend/models.py#L63)
   Содеожит данные о пользователе. Тип пользователя (сотрудник магазина или покупатель), e-mail, пароль, итд.
1. [Shop](https://github.com/fedor-metsger/el_shop/blob/a9bc5bf27d0dda60960f046876c2649292acf31d/backend/models.py#L109)
   Содержит описание магазина, который может создать пользователь.
1. [Category](https://github.com/fedor-metsger/el_shop/blob/a9bc5bf27d0dda60960f046876c2649292acf31d/backend/models.py#L128)
   Содержит описание категории товара в магазине.
1. [Product](https://github.com/fedor-metsger/el_shop/blob/a9bc5bf27d0dda60960f046876c2649292acf31d/backend/models.py#L141)
   Содержит общее описание продукта (название и категорию).
1. [ProductInfo](https://github.com/fedor-metsger/el_shop/blob/a9bc5bf27d0dda60960f046876c2649292acf31d/backend/models.py#L155)
   Содержит данные о наличии продукта в конкретном магазине (количество, цена, итд).
1. [Parameter](https://github.com/fedor-metsger/el_shop/blob/a9bc5bf27d0dda60960f046876c2649292acf31d/backend/models.py#L174)
   Содержит параметр описания продукта, например модель и цвет.
   Эти параметры могут отличаться от продукта к продукту.
1. [ProductParameter](https://github.com/fedor-metsger/el_shop/blob/a9bc5bf27d0dda60960f046876c2649292acf31d/backend/models.py#L186)
   Промежуточная модель, организует связь **многие ко многим**
   между продуктами и их наличием в магазине.
1. [Contact](https://github.com/fedor-metsger/el_shop/blob/a9bc5bf27d0dda60960f046876c2649292acf31d/backend/models.py#L202)
   Содержит данные о контакте пользователя. Используется при оформлении заказа.
   У одного пользователя может быть несколько контактов.
1. [Order](https://github.com/fedor-metsger/el_shop/blob/a9bc5bf27d0dda60960f046876c2649292acf31d/backend/models.py#L223)
   Содержит данные о заказе, сделанном покупателем.
1. [OrderItem](https://github.com/fedor-metsger/el_shop/blob/a9bc5bf27d0dda60960f046876c2649292acf31d/backend/models.py#L242)
   Содержит данные о конкретных позициях в заказе. Организует связь **многие ко многим**
   между заказами и наличием продукта в магазине.

### Frontend
Кроме того для работы над проектом и отладки был реализован модуль [frontend](https://github.com/fedor-metsger/el_shop/tree/main/frontend).

В этом модуле содержатся формы для просмотра данных, загруженных в БД.
Формы реализованы с помощью ЯП **JavaScript**.

## Docker и Docker Compose
Для упрощения развёртывания приложения в облаке были созданы файлы конфигурации:

- [docker-compose.yaml](docker-compose.yaml)
   Служит для конфигурации следующих сервисов:
  - db - конфигурация контейнера с СУБД **postgreSQL**
  - redis - конфигурация контейнера с СУБД **redis**
  - worker - конфигурация контейнера с процессом обработчиком задач **celery**
  - backend - конфигурация контейнера с ПО проекта
  - web - конфигурация контейнера с frontend-сервером **nginx**
  
- [Dockerfile](Dockerfile)
  Служит для сборки контейнеров **worker** и **backend**.
