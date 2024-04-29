# Модуль utils/auth.py
import streamlit as st
from postgre import async_connection
import asyncio
import os
# Подключение к базе данных
pg = async_connection.PG([os.environ.get("DB_CREDENTIALS", "")])

async def authenticate(email, password):
    """
    Функция аутентификации пользователя.

    Args:
        email (str): Адрес электронной почты пользователя.
        password (str): Пароль пользователя.

    Returns:
        bool: True, если аутентификация прошла успешно, иначе False.
    """
    # Выполняем запрос к базе данных для получения пользователя с указанным email и паролем
    users = await pg.fetch("SELECT * FROM users WHERE email = $1 AND password = $2", email, password)
    if users:
        return True
    else:
        return False
