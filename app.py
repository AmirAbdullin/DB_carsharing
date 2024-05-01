# import streamlit as st
# from pages import login, map_view 

# def main():
#     if 'page' not in st.session_state:
#         st.session_state['page'] = 'login'  

#     if st.session_state['page'] == 'login':
#         login.login_page()  
#     elif st.session_state['page'] == 'map' and 'user_id' in st.session_state:
#         map_view.show_map_view()  



# if __name__ == "__main__":
#     main()


import streamlit as st
from postgre import connect

def main():
    st.title("Сервис Аренды Автомобилей")

    menu = ["Главная", "Вход", "Регистрация"]
    choice = st.sidebar.selectbox("Меню", menu)
    if 'status' not in st.session_state:

        if choice == "Главная":
            st.subheader("Добро пожаловать")

        elif choice == "Вход":
            st.subheader("Вход")
            email = st.text_input("Email")
            password = st.text_input("Пароль", type="password")
            if st.button("Вход"):
                user = connect.sign_in_user(email, password)
                if user:
                    st.session_state['user_id'] = user[0]
                    st.success("Под логином {}".format(user[2]))
                    if user[2] == "admin":
                        st.session_state['status'] ='admin'
                        admin_dashboard()
                    elif user[2] == "worker":
                        st.session_state['status'] ='worker'
                        worker_dashboard()
                        
                    else:
                        st.session_state['status'] ='customer'
                        customer_dashboard(user[0])
                else:
                    st.error("Invalid Email or Password")

        elif choice == "Регистрация":
            st.subheader("Регистрация")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            user_info_id = st.text_input("User Info ID")
            if st.button("Регистрация"):
                connect.sign_up_user(email, password, user_info_id)
                st.success("You have successfully signed up")
                st.info("Go to Sign In to login")
    else:
        if st.session_state['status'] == 'admin':
            admin_dashboard()
        elif st.session_state['status'] =='worker':
            worker_dashboard()
        elif st.session_state['status'] == 'customer':
            customer_dashboard(user[0])
            
def admin_dashboard():
    st.subheader("Панель управления администратора")
    admin_menu = ["Посмотреть все машины", "Посмотреть всех пользователей", "Заблокировать/разблокировать пользователя", "История аренды",
                  "Все отзывы", "Изменить статус авто", "Добавить авто", "Убрать авто"]
    admin_choice = st.sidebar.selectbox("Admin Menu", admin_menu)

    if admin_choice == "Посмотреть все машины":
        cars = connect.view_all_cars()
        st.table(cars)

    elif admin_choice == "Посмотреть всех пользователей":
        users = connect.view_all_users()
        st.table(users)
    elif admin_choice == "Заблокировать/разблокировать пользователя":
        user_id = st.text_input("User ID")
        status = st.selectbox("Status", ["active", "blocked"])
        if st.button("Update"):
            connect.block_unblock_user(user_id, status)
            st.success("User status updated successfully")
    elif admin_choice == "История аренды":
        history = connect.view_travel_history()
        st.table(history)
    elif admin_choice == "Все отзывы":
        reviews = connect.view_all_reviews()
        st.table(reviews)
    elif admin_choice == "Изменить статус авто":
        car_id = st.text_input("Car ID")
        status = st.selectbox("Status", ["available", "rented"])
        if st.button("Update"):
            connect.change_car_status(car_id, status)
            st.success("Car status updated successfully")
    elif admin_choice == "Добавить авто":
        model_id = st.text_input("Model ID")
        rating_id = st.text_input("Rating ID")
        car_info_id = st.text_input("Car Info ID")
        price = st.text_input("Price")
        license_plate = st.text_input("License Plate")
        description = st.text_input("Description")
        location_id = st.text_input("Location ID")
        level = st.text_input("Level")
        if st.button("Add"):
            connect.add_car(model_id, rating_id, car_info_id, price, license_plate, description, location_id, level)
            st.success("Car added successfully")
    elif admin_choice == "Убрать авто":
        car_id = st.text_input("Car ID")
        if st.button("Remove"):
            connect.remove_car(car_id)
            st.success("Car removed successfully")

def worker_dashboard():
    st.subheader("Worker Dashboard")
    worker_menu = ["Add Car Info", "Edit Car Info"]
    worker_choice = st.sidebar.selectbox("Worker Menu", worker_menu)

    if worker_choice == "Add Car Info":
        year = st.text_input("Year")
        fuel = st.text_input("Fuel")
        color = st.text_input("Color")
        transmission = st.text_input("Transmission")
        fuel_type = st.text_input("Fuel Type")
        seats = st.text_input("Seats")
        if st.button("Add"):
            connect.add_car_info(year, fuel, color, transmission, fuel_type, seats)
            st.success("Car info added successfully")
    elif worker_choice == "Edit Car Info":
        car_info_id = st.text_input("Car Info ID")
        year = st.text_input("Year")
        fuel = st.text_input("Fuel")
        color = st.text_input("Color")
        transmission = st.text_input("Transmission")
        fuel_type = st.text_input("Fuel Type")
        seats = st.text_input("Seats")
        if st.button("Update"):
            connect.edit_car_info(car_info_id, year, fuel, color, transmission, fuel_type, seats)
            st.success("Car info updated successfully")

def customer_dashboard(user_info_id):
    st.subheader("Customer Dashboard")
    customer_menu = ["View Available Cars", "Rent Car", "Return Car", "Leave Review",
                     "View Trip History", "Edit User Data"]
    customer_choice = st.sidebar.selectbox("Customer Menu", customer_menu)

    if customer_choice == "View Available Cars":
        cars = connect.view_available_cars()
        st.table(cars)
    elif customer_choice == "Rent Car":
        car_id = st.text_input("Car ID")
        start_datetime = st.text_input("Start Datetime")
        end_datetime = st.text_input("End Datetime")
        pickup_location_id = st.text_input("Pickup Location ID")
        dropoff_location_id = st.text_input("Dropoff Location ID")
        total_price = st.text_input("Total Price")
        if st.button("Rent"):
            connect.rent_car(user_info_id, car_id, start_datetime, end_datetime, pickup_location_id, dropoff_location_id, total_price)
            st.success("Car rented successfully")
    elif customer_choice == "Return Car":
        rental_id = st.text_input("Rental ID")
        car_id = st.text_input("Car ID")
        if st.button("Return"):
            connect.return_car(rental_id, car_id)
            st.success("Car returned successfully")
    elif customer_choice == "Leave Review":
        car_id = st.text_input("Car ID")
        rating = st.text_input("Rating")
        comment = st.text_input("Comment")
        if st.button("Submit"):
            connect.leave_review(user_info_id, car_id, rating, comment)
            st.success("Review submitted successfully")
    elif customer_choice == "View Trip History":
        history = connect.view_trip_history(user_info_id)
        st.table(history)
    elif customer_choice == "Edit User Data":
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        phone_number = st.text_input("Phone Number")
        country = st.text_input("Country")
        city = st.text_input("City")
        birth_date = st.text_input("Birth Date")
        passport_id = st.text_input("Passport ID")
        issue_date = st.text_input("Issue Date")
        expiration_date = st.text_input("Expiration Date")
        if st.button("Update"):
            connect.edit_user_data(user_info_id, first_name, last_name, phone_number, country, city, birth_date, passport_id, issue_date, expiration_date)
            st.success("User data updated successfully")

if __name__ == '__main__':
    main()
