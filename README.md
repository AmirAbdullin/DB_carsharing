# DB_carsharing
Проект по созданию мультимодельной системы хранения информации

# **Настройка проекта:**
Скопируйте репозиторий:
```
git clone https://github.com/AmirAbdullin/DB_carsharing.git
```

# Создайте окружение (оптимально):
```
 python -m venv DB_carsharing

 DB_carsharing\Scripts\activate
```
#  Установите необходимые зависимости:
```
pip install -r requirements.txt
```

# Добавьте необходимые сертификаты для подключения к PostgreSQL:

```
mkdir -p ~/.postgresql && \
wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
     --output-document ~/.postgresql/root.crt && \
chmod 0600 ~/.postgresql/root.crt
```

# Запуститие Streamlit:

```
streamlit run app.py
```
