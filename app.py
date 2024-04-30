import streamlit as st
from pages import login, map_view  # Импортируем функции страниц из директории pages

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'  # Начальное состояние страницы

    # st.sidebar.title("Навигация")
    # page = st.sidebar.radio("Выберите страницу", ['login', 'map'])
    page = st.session_state['page']

    if page == 'login':
            login.login_page()  # Показываем страницу логина
    elif page == 'map' and 'user_id' in st.session_state:
        map_view.show_map_view()  # Показываем карту

    # # Отображаем страницу в зависимости от состояния
    # if page == 'login' or st.session_state['page'] == 'login':
    #     login.login_page()  # Показываем страницу логина
    #     if 'user_id' in st.session_state:  # Проверяем, есть ли ID пользователя в сессии
    #         st.session_state['page'] = 'map'  # Если авторизация прошла успешно, переключаемся на карту
    #         page = 'map'  # Обновляем текущую страницу на карту
    #         st.rerun()  # Перезапускаем приложение для отображения карты

    # if page == 'map' and 'user_id' in st.session_state:
    #     map_view.show_map_view()  # Показываем карту

if __name__ == "__main__":
    main()
