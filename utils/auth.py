# Модуль utils/auth.py
import streamlit as st


# Фиктивная база данных пользователей (можно заменить на реальную базу данных)
USERS = {
    "admin": "password123",  # Пример: имя пользователя и пароль
    "user1": "pass123",
    "user2": "securepass",
}

def login(username, password):
    """
    Функция аутентификации пользователя.

    Args:
        username (str): Имя пользователя.
        password (str): Пароль пользователя.

    Returns:
        bool: True, если аутентификация прошла успешно, иначе False.
    """
    # Получаем пароль из базы данных (здесь USERS - фиктивная база данных)
    stored_password = USERS.get(username)

    # Проверяем, соответствует ли введенный пароль сохраненному паролю
    if stored_password and password == stored_password:
        return True
    else:
        return False
