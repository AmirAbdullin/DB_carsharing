import streamlit as st
import pandas as pd
import numpy as np
import folium

# Фиктивная база данных машин
cars_data = {
    "CarID": [1, 2, 3, 4],
    "Latitude": [55.751244, 55.756487, 55.759865, 55.752126],  # Координаты широты
    "Longitude": [37.618423, 37.624989, 37.623815, 37.609227],  # Координаты долготы
    "Model": ["Tesla Model 3", "Toyota Corolla", "Honda Civic", "Ford Focus"],
    "Status": ["Free", "Occupied", "Free", "Free"]  # Статус машины
}

# Преобразование данных в DataFrame
df_cars = pd.DataFrame(cars_data)

def show_map_view():
    st.title("Карта доступных автомобилей")

    # Создание базовой карты с центром в центре Москвы
    map_center = [55.751244, 37.618423]  # Центр Москвы
    my_map = folium.Map(location=map_center, zoom_start=14)

    # Отображение машин на карте и обработка событий при клике на маркер
    for index, row in df_cars.iterrows():
        car_id = row["CarID"]
        model = row["Model"]
        status = row["Status"]
        latitude = row["Latitude"]
        longitude = row["Longitude"]

        if status == "Free":
            # Отметка на карте для свободной машины
            marker = folium.Marker(
                location=[latitude, longitude],
                popup=f"Car ID: {car_id}<br>Model: {model}<br>Status: {status}",
                icon=folium.Icon(color="green", icon="car")
            )
            marker.add_to(my_map)

            # Обработка события клика на маркере
            folium.Popup(f"Car ID: {car_id}").add_to(marker)
            marker.add_to(my_map)

            # Обработчик события для отображения информации об автомобиле под картой
            if st.button(f"Подробнее о машине ID {car_id}"):
                st.write(f"Модель: {model}")
                st.write(f"Статус: {status}")
                # Здесь можно добавить другие сведения об автомобиле

    # Преобразование карты в HTML
    map_html = my_map._repr_html_()

    # Отображение HTML с помощью st.components.v1.html
    st.components.v1.html(map_html, width=700, height=500)

# Определяем главную функцию для отображения карты
def main():
    show_map_view()

# Запуск основной функции приложения
if __name__ == "__main__":
    main()
