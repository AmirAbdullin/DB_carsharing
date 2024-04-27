import streamlit as st
import pandas as pd

# Фиктивная база данных пользователей
users_data = {
    "username": ["admin", "user1", "user2"],
    "email": ["admin@example.com", "user1@example.com", "user2@example.com"],
    "documents": ["Driver's License", "ID Card", "Passport"],
    "history": ["2023-04-01: Toyota Corolla rented", "2023-03-25: Tesla Model 3 rented", "2023-04-01: LADA rented"]
}

# Преобразование данных в DataFrame
df_users = pd.DataFrame(users_data)

def show_profile(username):
    st.title(f"Профиль пользователя: {username}")

    # Получение данных о пользователе
    user_info = df_users[df_users["username"] == username]

    if not user_info.empty:
        # Отображение основной информации о пользователе
        st.subheader("Основная информация")
        st.write(f"Имя пользователя: {username}")
        st.write(f"Электронная почта: {user_info['email'].values[0]}")

        # Отображение документов пользователя
        st.subheader("Документы пользователя")
        documents = user_info["documents"].values[0].split(", ")
        for document in documents:
            st.write(f"- {document}")

        # Отображение истории аренды
        st.subheader("История аренды")
        history = user_info["history"].values[0].split(", ")
        for event in history:
            st.write(f"- {event}")

    else:
        st.error("Пользователь не найден.")

# Определяем главную функцию для отображения страницы профиля
def main():
    # Получаем имя текущего пользователя (можно заменить на реальный механизм аутентификации)
    current_user = "admin"  # Пример: имя текущего пользователя

    show_profile(current_user)

# Запуск основной функции приложения
if __name__ == "__main__":
    main()
