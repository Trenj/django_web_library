root пользователь от базы на ноуте - 2005037

Таблица для пользователей в базу данных:
-SQL
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('user', 'admin')) NOT NULL DEFAULT 'user'
);

Добавление пользователя:
-SQL
INSERT INTO users (username, email, password_hash, full_name, role)
VALUES 
    ('user1', 'user1@example.com', 'hashed_password_1', 'Обычный Пользователь', 'user'),
    ('admin1', 'admin@example.com', 'hashed_password_2', 'Администратор', 'admin');
