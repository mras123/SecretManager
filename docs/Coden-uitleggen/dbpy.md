import mysql.connector
from flask import g as app_context_global

def db_connection():
    if 'db' not in app_context_global:
        # Your database connection details here
        app_context_global.db = mysql.connector.connect(
            host="localhost",
            user="secrets",
            password="BestPassword",
            database="secrets",
            port=5360
        )
        
# dit maakt de tables, en returns de database connectie in app_context_global.db
        create_users_table()
        create_secrets_table()
    return app_context_global.db

def create_users_table():
# dit maakt een cursor dat interact met de MySQL database  cursor is een pointer en je kan daardoor SQL commands excecuten en retrieve results van de database
    cursor = app_context_global.db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
# 
            id INT AUTO_INCREMENT PRIMARY KEY,
# email unique  betekend dat iedereen een andere email moet hebben en de NOT NULL betekened dat het niet niet null values heeft
            email VARCHAR(150) UNIQUE NOT NULL,
            username VARCHAR(150) NOT NULL,
# CHAR is een fixed-leght character om hashed passwors veilig opteslaan 
            password CHAR(64) NOT NULL
        )
    """)
    app_context_global.db.commit()
    cursor.close()

def create_secrets_table():
    cursor = app_context_global.db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secrets (
            id INT AUTO_INCREMENT PRIMARY KEY,
# integer field dat linkt elke secret naar de specefieke user (foreign key)
            user_id INT,
# dit is een TEXT field voor de secrets 
            content TEXT NOT NULL,
# dit linkt de user_id in de secrets table en de id in de users table linkt de secrets met een user
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    app_context_global.db.commit()
    cursor.close()

def teardown_db(exception):
    db = app_context_global.pop('db', None)
    if db is not None:
        db.close() 
