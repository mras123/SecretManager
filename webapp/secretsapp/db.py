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
        
       
        create_users_table()
        create_secrets_table()
    return app_context_global.db

def create_users_table():
    cursor = app_context_global.db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(150) UNIQUE NOT NULL,
            username VARCHAR(150) NOT NULL,
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
            user_id INT,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    app_context_global.db.commit()
    cursor.close()

def teardown_db(exception):
    db = app_context_global.pop('db', None)
    if db is not None:
        db.close()
