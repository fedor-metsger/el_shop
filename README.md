
# Проект «API сервиса заказа товаров для розничных сетей»

Проект выполнен в рамках дипломной работы к профессии **«Python-разработчик»**

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
Примет ответа при неправильных данных запроса:
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
Примет ответа при неправильных данных запроса:
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
Примет ответа при неправильных данных запроса:
```json
{
    "Status": true,
    "Удалено объектов": 0
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

1. [User](https://github.com/fedor-metsger/codeforces/blob/b3ad149efed885f5cae6c8dad59caa72636987b9/problems/models.py#L6C7-L6C10)
   Содеожит данные о пользователе. Тип пользователя (сотрудник магазина или покупатель), e-mail, пароль, итд.
1. [Shop](https://github.com/fedor-metsger/codeforces/blob/b3ad149efed885f5cae6c8dad59caa72636987b9/problems/models.py#L18)
   Содержит описание магазина, который может создать пользователь.
1. [Category](https://github.com/fedor-metsger/codeforces/blob/b3ad149efed885f5cae6c8dad59caa72636987b9/problems/models.py#L34)
   Содержит описание категории товара в магазине.
1. [Product](https://github.com/fedor-metsger/codeforces/blob/b3ad149efed885f5cae6c8dad59caa72636987b9/problems/models.py#L6C7-L6C10)
   Содержит общее описание продукта (название и категорию).
1. [ProductInfo](https://github.com/fedor-metsger/codeforces/blob/b3ad149efed885f5cae6c8dad59caa72636987b9/problems/models.py#L18)
   Содержит данные о наличии продукта в конкретном магазине (количество, цена, итд).
1. [Parameter](https://github.com/fedor-metsger/codeforces/blob/b3ad149efed885f5cae6c8dad59caa72636987b9/problems/models.py#L34)
   Содержит параметр описания продукта, например модель и цвет.
   Эти параметры могут отличаться от продукта к продукту.
1. [ProductParameter](https://github.com/fedor-metsger/codeforces/blob/b3ad149efed885f5cae6c8dad59caa72636987b9/problems/models.py#L6C7-L6C10)
   Промежуточная модель, организует связь **многие ко многим**
   между продуктами и их наличием в магазине.
1. [Contact](https://github.com/fedor-metsger/codeforces/blob/b3ad149efed885f5cae6c8dad59caa72636987b9/problems/models.py#L18)
   Содержит данные о контакте пользователя. Используется при оформлении заказа.
   У одного пользователя может быть несколько контактов.
1. [Order](https://github.com/fedor-metsger/codeforces/blob/b3ad149efed885f5cae6c8dad59caa72636987b9/problems/models.py#L34)
   Содержит данные о заказе, сделанном покупателем.
1. [OrderItem](https://github.com/fedor-metsger/codeforces/blob/b3ad149efed885f5cae6c8dad59caa72636987b9/problems/models.py#L6C7-L6C10)
   Содержит данные о конкретных позициях в заказе. Организует связь **многие ко многим**
   между заказами и наличием продукта в магазине.

### Frontend

Кроме того для работы над проектом и отладки был реализован модуль [frontend]().

В этом модуле содержатся формы для просмотра данных, загруженных в БД.
Формы реализованы с помощью ЯП **JavaScript**.
