# This sample data includes:
# - User types: admin and customer
# - Passports: two passport records
# - User personal info: two user personal info records
# - Users: two user records (one admin and one customer)
# - Driver licenses: two driver license records
# - Car brands: Toyota and Honda
# - Car models: Camry, Corolla, Civic, Accord
# - Cars info: two car info records
# - Locations: New York and Toronto
# - Car ratings: two car rating records
# - Cars: two car records
# - Rentals: two rental records
# - Rental extras: two rental extra records
# - Comments: two comment records
# - Reviews: two review records
# - Payments: two payment records

import psycopg2

conn = psycopg2.connect("""
    host=rc1d-fl2s62z7wxdz9gon.mdb.yandexcloud.net
    port=6432
    sslmode=verify-full
    dbname=carsharing
    user=user1
    password=
    target_session_attrs=read-write
""")

q = conn.cursor()

query = '''
-- Insert data into user_types table
INSERT INTO user_types (user_type, description, permissions)
VALUES
  ('admin', 'Administrator', 'all'),
  ('customer', 'Regular customer', 'basic');

-- Insert data into passports table
INSERT INTO passports (passport_number, gender)
VALUES
  (123456789, 'Male'),
  (987654321, 'Female');

-- Insert data into user_personal_info table
INSERT INTO user_personal_info (first_name, last_name, phone_number, country, city, birth_date, passport_id, issue_date, expiration_date)
VALUES
  ('John', 'Doe', '1234567890', 'USA', 'New York', '1990-01-01', '1', '2020-01-01', '2030-01-01'),
  ('Jane', 'Smith', '9876543210', 'Canada', 'Toronto', '1995-05-10', '2', '2021-02-15', '2031-02-15');

-- Insert data into users table
INSERT INTO users (email, password, user_info_id, status, user_type)
VALUES
  ('john@example.com', 'password123', 1, 'active', 'admin'),
  ('jane@example.com', 'password456', 2, 'active', 'customer');

-- Insert data into driver_licenses table
INSERT INTO driver_licenses (user_id, license_number, expiration_date)
VALUES
  (1, 'ABC123', '2025-01-01'),
  (2, 'XYZ789', '2026-05-10');

-- Insert data into car_brands table
INSERT INTO car_brands (name)
VALUES
  ('Toyota'),
  ('Honda');

-- Insert data into car_models table
INSERT INTO car_models (brand_id, name)
VALUES
  (1, 'Camry'),
  (1, 'Corolla'),
  (2, 'Civic'),
  (2, 'Accord');

-- Insert data into cars_info table
INSERT INTO cars_info (year, fuel, color, transmission, fuel_type, seats)
VALUES
  (2020, 50.5, 'Red', 'Automatic', 'Gasoline', 5),
  (2019, 60.2, 'Blue', 'Manual', 'Diesel', 5);

-- Insert data into locations table
INSERT INTO locations (latitude, longitude, address, city)
VALUES
  (40.7128, -74.0060, '123 Main St', 'New York'),
  (43.6532, -79.3832, '456 Elm St', 'Toronto');

-- Insert data into car_ratings table
INSERT INTO car_ratings (rating, number_reviews)
VALUES
  (4.5, 10),
  (4.2, 5);

-- Insert data into cars table
INSERT INTO cars (model_id, rating_id, car_info_id, price, license_plate, available, status, description, location_id, level)
VALUES
  (1, 1, 1, 50.00, 'ABC123', true, 'available', 'Lorem ipsum dolor sit amet', 1, 1),
  (3, 2, 2, 60.00, 'XYZ789', true, 'available', 'Consectetur adipiscing elit', 2, 2);

-- Insert data into rentals table
INSERT INTO rentals (user_id, car_id, start_datetime, end_datetime, pickup_location_id, dropoff_location_id, total_price, payment_status, status)
VALUES
  (1, 1, '2023-06-01 10:00:00', '2023-06-05 18:00:00', 1, 1, 250.00, 'paid', 'completed'),
  (2, 2, '2023-06-10 14:30:00', '2023-06-12 12:00:00', 2, 2, 120.00, 'pending', 'upcoming');

-- Insert data into rental_extras table
INSERT INTO rental_extras (rental_id, description, special_price)
VALUES
  (1, 'GPS Navigation', 10.00),
  (2, 'Child Seat', 15.00);

-- Insert data into comments table
INSERT INTO comments (comment)
VALUES
  ('Great car, smooth ride!'),
  ('Excellent service, highly recommended.');

-- Insert data into reviews table
INSERT INTO reviews (user_id, car_id, rating, comment_id)
VALUES
  (1, 1, 5, 1),
  (2, 2, 4, 2);

  insert into levels(level_id, level) values (1, 'Elite'), (2, 'Standart')


-- Insert data into payments table
INSERT INTO payments (rental_id, amount, payment_method, status)
VALUES
  (1, 250.00, 'Credit Card', 'completed'),
  (2, 120.00, 'PayPal', 'pending');
'''

q.execute(query)


conn.close()