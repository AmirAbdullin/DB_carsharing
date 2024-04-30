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
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  user_info_id INTEGER,
  status VARCHAR(50),
  user_type VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_personal_info (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  phone_number VARCHAR(20),
  country VARCHAR(50),
  city VARCHAR(50),
  birth_date VARCHAR(20),
  passport_id INTEGER,
  issue_date VARCHAR(20),
  expiration_date VARCHAR(20)
);

CREATE TABLE passports (
  id SERIAL PRIMARY KEY,
  passport_number INTEGER,
  gender VARCHAR(10)
);

CREATE TABLE user_types (
  id SERIAL PRIMARY KEY,
  user_type VARCHAR(50) UNIQUE,
  description VARCHAR(255),
  permissions VARCHAR(255)
);

CREATE TABLE driver_licenses (
  id SERIAL PRIMARY KEY,
  user_id INTEGER UNIQUE,
  license_number VARCHAR(50),
  expiration_date DATE
);

CREATE TABLE car_brands (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50)
);

CREATE TABLE car_models (
  id SERIAL PRIMARY KEY,
  brand_id INTEGER,
  name VARCHAR(50)
);

CREATE TABLE cars (
  id SERIAL PRIMARY KEY,
  model_id INTEGER,
  rating_id INTEGER,
  car_info_id INTEGER,
  price FLOAT,
  license_plate VARCHAR(20) UNIQUE,
  available BOOLEAN DEFAULT true,
  status VARCHAR(50),
  description TEXT,
  location_id INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  level integer
);

CREATE TABLE cars_info (
  id SERIAL PRIMARY KEY,
  year INTEGER,
  fuel DECIMAL,
  color VARCHAR(50),
  transmission VARCHAR(50),
  fuel_type VARCHAR(50),
  seats INTEGER
);

CREATE TABLE rentals (
  id SERIAL PRIMARY KEY,
  user_id INTEGER,
  car_id INTEGER,
  start_datetime TIMESTAMP,
  end_datetime TIMESTAMP,
  pickup_location_id INTEGER,
  dropoff_location_id INTEGER,
  total_price DECIMAL,
  payment_status VARCHAR(50),
  status VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rental_extras (
  id SERIAL PRIMARY KEY,
  rental_id INTEGER,
  description TEXT,
  special_price DECIMAL
);

CREATE TABLE reviews (
  id SERIAL PRIMARY KEY,
  user_id INTEGER,
  car_id INTEGER,
  rating INTEGER,
  comment_id INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  comment VARCHAR(255)
);

CREATE TABLE car_ratings (
  id SERIAL PRIMARY KEY,
  rating DECIMAL,
  number_reviews INTEGER
);

CREATE TABLE locations (
  id SERIAL PRIMARY KEY,
  latitude DECIMAL,
  longitude DECIMAL,
  address VARCHAR(255),
  city VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments (
  id SERIAL PRIMARY KEY,
  rental_id INTEGER,
  amount DECIMAL,
  payment_method VARCHAR(50),
  status VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE levels (
  level_id SERIAL PRIMARY KEY,
  level varchar(50)
);

ALTER TABLE users ADD FOREIGN KEY (user_type) REFERENCES user_types (user_type);
ALTER TABLE users ADD FOREIGN KEY (user_info_id) REFERENCES user_personal_info (id);
ALTER TABLE cars ADD FOREIGN KEY (car_info_id) REFERENCES cars_info (id);
ALTER TABLE cars ADD FOREIGN KEY (level) REFERENCES levels (level_id);
ALTER TABLE user_personal_info ADD FOREIGN KEY (passport_id) REFERENCES passports (id);
ALTER TABLE driver_licenses ADD FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE car_models ADD FOREIGN KEY (brand_id) REFERENCES car_brands (id);
ALTER TABLE cars ADD FOREIGN KEY (model_id) REFERENCES car_models (id);
ALTER TABLE cars ADD FOREIGN KEY (location_id) REFERENCES locations (id);
ALTER TABLE cars ADD FOREIGN KEY (rating_id) REFERENCES car_ratings (id);
ALTER TABLE rentals ADD FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE rentals ADD FOREIGN KEY (car_id) REFERENCES cars (id);
ALTER TABLE rental_extras ADD FOREIGN KEY (rental_id) REFERENCES rentals (id);
ALTER TABLE

reviews ADD FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE reviews ADD FOREIGN KEY (car_id) REFERENCES cars (id);
ALTER TABLE rentals ADD FOREIGN KEY (pickup_location_id) REFERENCES locations (id);
ALTER TABLE rentals ADD FOREIGN KEY (dropoff_location_id) REFERENCES locations (id);
ALTER TABLE payments ADD FOREIGN KEY (rental_id) REFERENCES rentals (id);
ALTER TABLE reviews ADD FOREIGN KEY (comment_id) REFERENCES comments (id);


'''

q.execute(query)

# print(q.fetch())

conn.close()
