import streamlit as st
from pages import login, map_view  # Импортируем функции страниц из директории pages
from postgre import async_connection
import asyncio
import os


pg = async_connection.PG([os.environ.get("DB_CREDENTIALS", "")])


async def main():
    print(await pg.get_table("users"))
    
    st.sidebar.title("Навигация")  # Заголовок боковой панели (sidebar) для навигации

    # Создаем словарь для хранения названий страниц и соответствующих функций
    pages = {
        "Авторизация": login.login_page,
        #"Карта автомобилей": map_view.show_map_view
    }

    # Добавляем в боковую панель радиокнопки для выбора страницы
    selected_page = st.sidebar.radio("Выберите страницу", list(pages.keys()))

    # Запускаем функцию выбранной страницы
    pages[selected_page]()

asyncio.run(main())
