import streamlit as st
import pandas as pd
import folium
import asyncio
import os
from postgre import async_connection

# Подключаемся к базе данных
pg = async_connection.PG([os.environ.get("DB_CREDENTIALS", "")])

# Определяем главную функцию для отображения карты
async def show_map_view():
    st.title("Карта всех автомобилей")

    # Получаем данные об уровнях автомобилей из базы данных
    levels_query = "SELECT * FROM levels;"
    levels_data = await pg.fetch(levels_query)
    levels_dict = {level['level_id']: level['level'] for level in levels_data}

    # Выбор уровня автомобиля
    level_id = st.selectbox("Выберите уровень автомобиля:", options=["Все"] + list(levels_dict.values()))

    # Формирование условия для SQL-запроса
    condition = ""
    if level_id != "Все":
        condition = f"WHERE levels.level = '{level_id}'"

    # Запрос данных о машинах и их координатах из базы данных с учетом выбранного уровня
    cars_query = f"""
    SELECT cars.*, locations.latitude, locations.longitude, levels.level
    FROM cars 
    JOIN locations ON cars.location_id = locations.id
    JOIN levels ON cars.level = levels.level_id
    {condition};
    """
    cars_data = await pg.fetch(cars_query)

    # Создание базовой карты с центром в центре Москвы
    map_center = [55.751244, 37.618423]  # Центр Москвы
    my_map = folium.Map(location=map_center, zoom_start=14)

    # Определение цветов для разных уровней автомобилей
    level_colors = {
        'Elite': "purple",  # Elite
        'Stadnart': "cadetblue",   # Standard
    }

    # Отображение машин на карте
    for car in cars_data:
        car_id = car['id']
        latitude = car['latitude']
        longitude = car['longitude']
        level = car['level']

        # Определение цвета значка в зависимости от уровня автомобиля
        icon_color = level_colors.get(level, "gray")

        # Отметка на карте для машины
        popup_html = f"<b>Car ID:</b> {car_id}<br><b>Status:</b> {car['status']}<br><b>Description:</b> {car['description']}"
        marker = folium.Marker(
            location=[latitude, longitude],
            popup=popup_html,
            icon=folium.Icon(color=icon_color, icon="car", prefix="fa")
        )
        marker.add_to(my_map)

    # Преобразование карты в HTML
    map_html = my_map._repr_html_()

    # Отображение HTML с помощью st.components.v1.html
    st.components.v1.html(map_html, width=700, height=500)

# Определяем главную функцию для запуска приложения
async def main():
    await show_map_view()

# Запуск основной функции приложения
if __name__ == "__main__":
    asyncio.run(main())
