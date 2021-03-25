# UnitPay-PythonAPI

![Image alt](https://img.shields.io/badge/python-%203.9-blue)
![Image alt](https://img.shields.io/badge/current%20version-1.0.1-green)
![Image alt](https://img.shields.io/badge/Developer-WeRn-red)

UnitPay python API

### Инструкция по установке:

**1. Заходим в config.py и изменяем данные для подключения к базе данных и вводим свой секретный ключ от UnitPay:**
```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/aion?charset=utf8mb4'
UNITPAY_SECRET_KEY = '00000000000000000000'
```

**2. Воссоздание таблицы для храненя платежей:**
```
В models.py находятся модели таблиц базы данных - в своем MySQL сервере необходимо
воссоздать таблицe unitpay_payments - по аналогии модели.
А также проверить совпадает ли таблица account_data, если нет - внести коррективы
```

**3. Установить зависимые библиотеки для работы API через консоль Windows/Linux:**
```
pip3 install flask pymysql flask-sqlalchemy 
```

**4. Запустить API:**
```
python api.py
И API будет доступен по адресу http://127.0.0.1:8080
```

**5. На стороне UnitPay указать обработчик платежей:**
```
Он будет доступен по адресу: {ВашДомен}/api/v1.0/unitpay/payment/
```
