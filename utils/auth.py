# Модуль utils/auth.py
import streamlit as st
from postgre import connect  # Убедитесь, что класс PG адаптирован под psycopg2
import os
import sys
sys.path.append(os.path.abspath("./../postgre"))

# Подключение к базе данных
pg = connect()  # Создание экземпляра класса для работы с базой данных

def authenticate(email, password):
    """
    Функция аутентификации пользователя.
    
    Args:
        email (str): Адрес электронной почты пользователя.
        password (str): Пароль пользователя.

    Returns:
        bool: True, если аутентификация прошла успешно, иначе False.
    """
    query = f"SELECT id FROM users WHERE email = '{email}' AND password = '{password}'"
    user = connect.fetch_all(query)  # Используем execute_query для синхронного запроса
    if user:
        return True
    else:
        return False
