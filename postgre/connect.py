import psycopg2
import os
from random import randint

def fetch_all(query):
    cur = None
    conn = None
    result = None
    try:
        conn = psycopg2.connect(os.environ.get("DB_CREDENTIALS"))
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
    except Exception as ex:
        print(f'EXCEPTION [fetch_all({query})]:', ex)
    if cur:
        cur.close()
    if conn:
        conn.close()
    return result


def query_commit(query):
    cur = None
    conn = None
    result = None
    try:
        conn = psycopg2.connect(os.environ.get("DB_CREDENTIALS"))
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except Exception as ex:
        print(f'EXCEPTION [commit({query})]:', ex)
    if cur:
        cur.close()
    if conn:
        conn.close()
    


def sign_in_user(login, password):
    query = f"SELECT user_info_id, status, user_type FROM users WHERE email = '{login}' AND password = '{password}'"
    user = fetch_all(query)
    if user:
        return user[0]
    return False


def check_user_exists(login):
    query = f"SELECT id WHERE email = '{login}'"
    user = fetch_all(query)
    return len(user) > 0


def sign_up_user(login, password):
    query = f'''INSERT INTO users (email, password, user_info_id, status, user_type)
    VALUES
  ('{login}', '{password}', '{randint(0, 1000000000)}', 'active', 'customer')'''
    query_commit(query)
    
# Admin Queries
def view_all_cars():
    query = "SELECT * FROM cars;"
    return fetch_all(query)


def view_all_users():
    query = "SELECT * FROM users;"
    return fetch_all(query)


def block_unblock_user(user_id, status):
    query = f"UPDATE users SET status = '{status}' WHERE id = {user_id};"
    query_commit(query)


def view_travel_history():
    query = '''
    SELECT u.email, r.start_datetime, r.end_datetime, c.license_plate, r.total_price
    FROM rentals r
    JOIN users u ON r.user_id = u.id
    JOIN cars c ON r.car_id = c.id;
    '''
    return fetch_all(query)


def view_all_reviews():
    query = '''
    SELECT u.email, c.license_plate, r.rating, c.comment
    FROM reviews r
    JOIN users u ON r.user_id = u.id
    JOIN cars c ON r.car_id = c.id
    JOIN comments c ON r.comment_id = c.id;
    '''
    return fetch_all(query)


def change_car_status(car_id, status):
    query = f"UPDATE cars SET status = '{status}' WHERE id = {car_id};"
    query_commit(query)


def add_car(model_id, rating_id, car_info_id, price, license_plate, description, location_id, level):
    query = f'''
    INSERT INTO cars (model_id, rating_id, car_info_id, price, license_plate, available, status, description, location_id, level)
    VALUES ({model_id}, {rating_id}, {car_info_id}, {price}, '{license_plate}', true, 'available', '{description}', {location_id}, {level});
    '''
    query_commit(query)


def remove_car(car_id):
    query = f"DELETE FROM cars WHERE id = {car_id};"
    query_commit(query)


# Customer Queries
def sign_up_user(email, password, user_info_id):
    query = f'''
    INSERT INTO users (email, password, user_info_id, status, user_type)
    VALUES ('{email}', '{password}', {user_info_id}, 'active', 'customer');
    '''
    query_commit(query)


def sign_in_user(email, password):
    query = f"SELECT user_info_id, status, user_type FROM users WHERE email = '{email}' AND password = '{password}';"
    user = fetch_all(query)
    if user:
        return user[0]
    return False


def edit_user_data(user_info_id, first_name, last_name, phone_number, country, city, birth_date, passport_id, issue_date, expiration_date):
    query = f'''
    UPDATE user_personal_info
    SET first_name = '{first_name}',
        last_name = '{last_name}',
        phone_number = '{phone_number}',
        country = '{country}',
        city = '{city}',
        birth_date = '{birth_date}',
        passport_id = {passport_id},
        issue_date = '{issue_date}',
        expiration_date = '{expiration_date}'
    WHERE id = {user_info_id};
    '''
    query_commit(query)


def view_available_cars():
    query = '''
    SELECT c.*, b.name AS brand, m.name AS model
    FROM cars c
    JOIN car_models m ON c.model_id = m.id
    JOIN car_brands b ON m.brand_id = b.id
    WHERE c.available = true;
    '''
    return fetch_all(query)


def rent_car(user_id, car_id, start_datetime, end_datetime, pickup_location_id, dropoff_location_id, total_price):
    query = f'''
    INSERT INTO rentals (user_id, car_id, start_datetime, end_datetime, pickup_location_id, dropoff_location_id,

total_price, payment_status, status)
    VALUES ({user_id}, {car_id}, '{start_datetime}', '{end_datetime}', {pickup_location_id}, {dropoff_location_id}, {total_price}, 'pending', 'active');
    '''
    query_commit(query)

    query = f"UPDATE cars SET available = false, status = 'rented' WHERE id = {car_id};"
    query_commit(query)


def return_car(rental_id, car_id):
    query = f"UPDATE rentals SET status = 'completed' WHERE id = {rental_id};"
    query_commit(query)

    query = f"UPDATE cars SET available = true, status = 'available' WHERE id = {car_id};"
    query_commit(query)


def leave_review(user_id, car_id, rating, comment):
    query = f"INSERT INTO comments (comment) VALUES ('{comment}');"
    query_commit(query)

    query = f'''
    INSERT INTO reviews (user_id, car_id, rating, comment_id)
    VALUES ({user_id}, {car_id}, {rating}, CURRVAL('comments_id_seq'));
    '''
    query_commit(query)


def view_trip_history(user_id):
    query = f'''
    SELECT r.start_datetime, r.end_datetime, c.license_plate, r.total_price
    FROM rentals r
    JOIN cars c ON r.car_id = c.id
    WHERE r.user_id = {user_id};
    '''
    return fetch_all(query)


# Worker Queries
def add_car_info(year, fuel, color, transmission, fuel_type, seats):
    query = f'''
    INSERT INTO cars_info (year, fuel, color, transmission, fuel_type, seats)
    VALUES ({year}, {fuel}, '{color}', '{transmission}', '{fuel_type}', {seats});
    '''
    query_commit(query)

    query = f'''
    INSERT INTO cars (model_id, rating_id, car_info_id, price, license_plate, available, status, description, location_id, level)
    VALUES (<model_id>, <rating_id>, CURRVAL('cars_info_id_seq'), <price>, '<license_plate>', true, 'available', '<description>', <location_id>, <level>);
    '''
    query_commit(query)


def edit_car_info(car_info_id, year, fuel, color, transmission, fuel_type, seats):
    query = f'''
    UPDATE cars_info
    SET year = {year},
        fuel = {fuel},
        color = '{color}',
        transmission = '{transmission}',
        fuel_type = '{fuel_type}',
        seats = {seats}
    WHERE id = {car_info_id};
    '''
    query_commit(query)
