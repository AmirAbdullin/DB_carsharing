from postgre import connect  # Используйте ваш модуль для работы с БД
import os
import sys
sys.path.append(os.path.abspath("./../postgre"))
import streamlit as st

def show_user_profile(user_id):
    print(user_id)
    query = """
    SELECT first_name, last_name, phone_number, country, city, birth_date, issue_date, expiration_date
    FROM user_personal_info
    WHERE id = '{user_id[0]}';
    """
    user_info = connect.fetch_all(query) 
    if user_info:
        user_info = user_info[0]
        st.write(f"**First Name:** {user_info[0]}")
        st.write(f"**Last Name:** {user_info[1]}")
        st.write(f"**Phone Number:** {user_info[2]}")
        st.write(f"**Country:** {user_info[3]}")
        st.write(f"**City:** {user_info[4]}")
        st.write(f"**Birth Date:** {user_info[5].strftime('%Y-%m-%d')}")
        st.write(f"**Passport Issue Date:** {user_info[6].strftime('%Y-%m-%d')}")
        st.write(f"**Passport Expiration Date:** {user_info[7].strftime('%Y-%m-%d')}")
    else:
        st.error("User not found!")


# Определяем главную функцию для отображения страницы профиля
def main():
    # Получаем имя текущего пользователя (можно заменить на реальный механизм аутентификации)
    # current_user = user_id  # Пример: имя текущего пользователя

    show_user_profile(st.session_state["user_id"])

# Запуск основной функции приложения
if __name__ == "__main__":
    main()
