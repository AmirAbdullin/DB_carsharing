import streamlit as st
import pandas as pd
import numpy as np
import folium

# Фиктивная база данных машин с дополнительной информацией
cars_data = {
    "CarID": [1, 2, 3, 4],
    "Latitude": [55.751244, 55.756487, 55.759865, 55.752126],  # Координаты широты
    "Longitude": [37.618423, 37.624989, 37.623815, 37.609227],  # Координаты долготы
    "Model": ["Tesla Model 3", "Toyota Corolla", "Honda Civic", "Ford Focus"],
    "Status": ["Free", "Occupied", "Free", "Free"],  # Статус машины
    "FuelLevel": [80, 60, 75, 90],  # Уровень топлива
    "PricePerHour": [1500, 800, 700, 600],  # Стоимость аренды в час
    "EliteLevel": ["Luxury", "Standard", "Standard", "Economy"]  # Уровень элитарности
}


# Преобразование данных в DataFrame
df_cars = pd.DataFrame(cars_data)

def show_map_view():
    st.title("Карта доступных автомобилей")

    # Выбор группы автомобилей
    elite_levels = df_cars["EliteLevel"].unique()
    selected_level = st.selectbox("Выберите уровень элитарности:", elite_levels)

    # Создание базовой карты с центром в центре Москвы
    map_center = [55.751244, 37.618423]  # Центр Москвы
    my_map = folium.Map(location=map_center, zoom_start=14)

    # Отображение машин на карте
    for index, row in df_cars.iterrows():
        if row["EliteLevel"] == selected_level:
            car_id = row["CarID"]
            model = row["Model"]
            status = row["Status"]
            latitude = row["Latitude"]
            longitude = row["Longitude"]

            # Отметка на карте для свободной машины
            icon_color = "purple" if selected_level == "Luxury" else  "green"
            marker = folium.Marker(
                location=[latitude, longitude],
                popup=f"Car ID: {car_id}<br>Model: {model}<br>Status: {status}",
                icon=folium.Icon(color=icon_color, icon="car", prefix = "fa")
            )
            marker.add_to(my_map)

            # Обработчик события для отображения информации об автомобиле
            if st.button(f"Подробнее о машине ID {car_id}"):
                st.write(f"**Модель:** {model}")
                st.write(f"**Статус:** {status}")
                st.write(f"**Уровень топлива:** {row['FuelLevel']}%")
                st.write(f"**Стоимость аренды в час:** {row['PricePerHour']} руб.")
                st.image("Tesla.png", caption="Фото автомобиля", width=300)

                # Дополнительная информация и кнопка "Забронировать"
                st.write(f"**Государственный номер:** {generate_license_plate()}")  # Генерация номера
                st.button("Забронировать")

    # Преобразование карты в HTML
    map_html = my_map._repr_html_()

    # Отображение HTML с помощью st.components.v1.html
    st.components.v1.html(map_html, width=700, height=500)

def generate_license_plate():
    """Генерация случайного государственного номера."""
    return f"{chr(65 + np.random.randint(0, 26))}{np.random.randint(100, 999)}{chr(65 + np.random.randint(0, 26))}"

# Определяем главную функцию для отображения карты
def main():
    show_map_view()

# Запуск основной функции приложения
if __name__ == "__main__":
    main()
