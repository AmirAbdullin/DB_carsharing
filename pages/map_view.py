from pages.profile import show_user_profile
import streamlit as st
import pandas as pd
import folium
from postgre import connect  
import os
import sys
sys.path.append(os.path.abspath("./../postgre"))


def show_map_view():
    if 'user_id' in st.session_state:
        if st.button("Профиль"):
            show_user_profile(st.session_state['user_id'])
            
    st.title("Карта всех автомобилей")

    # Получаем данные об уровнях автомобилей из базы данных
    levels_query = "SELECT * FROM levels;"
    levels_data = connect.fetch_all(levels_query)
    levels_dict = {level[0]: level[1] for level in levels_data}

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
    cars_data = connect.fetch_all(cars_query)

    # Создание базовой карты с центром в центре Москвы
    map_center = [55.751244, 37.618423]  # Центр Москвы
    my_map = folium.Map(location=map_center, zoom_start=14)

    # Определение цветов для разных уровней автомобилей
    level_colors = {
        'Elite': "purple",  # Elite
        'Stadnart': "yellow",   # Standard
    }

    # Отображение машин на карте
    for car in cars_data:
        car_id = car[0]
        latitude = car[13]
        longitude = car[14]
        level = car[15]
        car_price = car[4]  # Предположим, что статус - это пятый элемент в кортеже
        license_plate = car[5]

        # Определение цвета значка в зависимости от уровня автомобиля
        icon_color = level_colors.get(level, "gray")

        # Отметка на карте для машины
        popup_html = f"""
    <b>Car ID:</b> {car_id}<br>
    <b>Price:</b> {car_price}<br>
    <b>license_plate:</b> {license_plate}<br>
    <b>Coordinates:</b> Latitude {latitude}, Longitude {longitude}
    """
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

    

def main():
    show_map_view()

if __name__ == "__main__":
    st.set_page_config(page_title="map", layout="wide")
    main()
