import streamlit as st
from postgre import async_connection
import asyncio
import os

# Определение переменных
PAGE_LOGIN = "Login"
PAGE_MAP_VIEW = "Map View"

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

async def login_page():
    """
    Функция для отображения страницы авторизации.
    """
    st.title("Авторизация")

    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        if await authenticate(email, password):
            # Успешная авторизация
            st.success("Успешная авторизация!")
            # Устанавливаем состояние страницы на MAP_VIEW
            st.session_state["page"] = PAGE_MAP_VIEW
        else:
            st.error("Неверные учетные данные. Пожалуйста, попробуйте снова.")

# Функция для отображения страницы карты
def show_map_view():
    """
    Функция для отображения страницы карты.
    """
    st.title("Карта доступных автомобилей")
    st.write("Здесь будет отображена карта с доступными автомобилями")

# Определяем главную функцию приложения
async def main():
    # Инициализация состояния страницы, если оно не определено
    if "page" not in st.session_state:
        st.session_state["page"] = PAGE_LOGIN

    # Определение условий для переключения между страницами
    if st.session_state["page"] == PAGE_LOGIN:
        await login_page()
    elif st.session_state["page"] == PAGE_MAP_VIEW:
        show_map_view()

# Запуск основной функции приложения
if __name__ == "__main__":
    asyncio.run(main())
