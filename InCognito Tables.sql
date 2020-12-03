CREATE TABLE IF NOT EXISTS users(
user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
user_name VARCHAR(50) UNIQUE NOT NULL,
hashed_password VARCHAR(1000) NOT NULL,
email VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS contacts(
user_id INT NOT NULL REFERENCES users(user_id),
contact_id INT NOT NULL REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS pke(
user_id INT NOT NULL REFERENCES users(user_id),
user_pke VARCHAR(1000)
);

CREATE TABLE IF NOT EXISTS messages(
message_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
sender INT REFERENCES users(user_id),
receiver INT REFERENCES users(user_id),
message TEXT,
timestamp INT NOT NULL
);