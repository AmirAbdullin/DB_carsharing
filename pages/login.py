import streamlit as st
from utils.auth import login

# Определим состояние страницы авторизации
PAGE_LOGIN = "Login"
PAGE_MAP_VIEW = "Map View"

def login_page():
    st.title("Авторизация")

    username = st.text_input("Имя пользователя")
    password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        if login(username, password):  # Исправленный вызов функции login
            # Успешная авторизация
            st.success("Успешная авторизация!")
            # Устанавливаем состояние страницы на MAP_VIEW
            st.session_state["page"] = PAGE_MAP_VIEW
        else:
            st.error("Неверные учетные данные. Пожалуйста, попробуйте снова.")

# Функция для отображения страницы карты
def show_map_view():
    st.title("Карта доступных автомобилей")
    st.write("Здесь будет отображена карта с доступными автомобилями")

# Определяем главную функцию приложения
def main():
    # Инициализация состояния страницы, если оно не определено
    if "page" not in st.session_state:
        st.session_state["page"] = PAGE_LOGIN

    # Определение условий для переключения между страницами
    if st.session_state["page"] == PAGE_LOGIN:
        login_page()
    elif st.session_state["page"] == PAGE_MAP_VIEW:
        show_map_view()

# Запуск основной функции приложения
if __name__ == "__main__":
    main()
