CREATE DATABASE bookdb;
USE bookdb;

CREATE TABLE users(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(255),
    created_date DATE
);


CREATE TABLE books(
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(50),
    author VARCHAR(50),
    added_date DATE,
    status VARCHAR(50) DEFAULT 'Reading',
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
