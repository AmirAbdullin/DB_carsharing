import os
import sys
sys.path.append(os.path.abspath("./../postgre"))
import streamlit as st
from postgre import connect



# Определение переменных
PAGE_LOGIN = "login"
PAGE_MAP_VIEW = "map"

# Подключение к базе данных

def login_page():
    st.title("Авторизация")
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        user_id = connect.sign_in_user(email, password)
        if user_id:
            st.success("Успешная авторизация!")
            st.session_state["user_id"] = user_id
            st.session_state["page"] = "map"
            st.rerun()
        else:
            st.error("Неверные учетные данные.")

def show_map_view():
    """
    Функция для отображения страницы карты.
    """
    st.title("Карта доступных автомобилей")
    st.write("Здесь будет отображена карта с доступными автомобилями")

def main():
    """
    Главная функция приложения для управления страницами.
    """
    if "page" not in st.session_state:
        st.session_state["page"] = PAGE_LOGIN

    if st.session_state["page"] == PAGE_LOGIN:
        login_page()
    # elif st.session_state["page"] == PAGE_MAP_VIEW:
    #     show_map_view()

if __name__ == "__main__":
    main()
