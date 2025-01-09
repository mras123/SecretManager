# re is voor meer veiliging en string manipulatie
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from hashlib import sha256  # For password hashing
from .db import db_connection  # Import the db_connection function
from datetime import datetime, timedelta
import re


bp = Blueprint("home", __name__)

@bp.route("/")
def index():
# dit checkt de user_id in de session en stored users data door meerdere requests
    if 'user_id' in session:
# dit functie haalt de user informatie in de user_id in de sessions
        user = get_user_by_id(session['user_id'])
# dit checkt of de user bestaat user_id
        if user:
# als een user inlogged wordt hij gegroet met de string  hello en de meta tag is voor de refreshing van de pagia met 0 seconden delay en redircts naar de volgende URL
            return f"Hello, {user['username']}! <meta http-equiv='refresh' content='0;URL=http://127.0.0.1:5000/create_secret' />"
    return render_template("home/index.html")
# get en post zijn http methods voor display de login GET en en procces from data POST
@bp.route('/login', methods=['GET', 'POST'])
def login():
# dit checkt of de HTTP request POST is als de user de login form submmits en de username en password requests in de form 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
# dit haalt de user informatie uit de database met de username
        user = get_user_by_username(username)

        if user:
            hashed_password = sha256(password.encode()).hexdigest()
# dit checkt de hashes password in de form met de hashed password in de database voor de user als ze matchen word de user ingelogged
            if user['password'] == hashed_password:
                session['user_id'] = user['id']

                # Update the last login time in the database
# dit maakt een DB connection 
                db = db_connection()
# db cursor een cursos is een db object geberuikt om SQL queries uitevoeren
                cursor = db.cursor()
# cursor execute is een SQL update statement en update statments in de users table en zet de last_login fielt naar huidige tijd door ne NOW funcite 
                cursor.execute("UPDATE users SET last_login = NOW() WHERE id = %s", (user['id'],))
# commit slaat de veranderingen in de database op
                db.commit()
                cursor.close()

                flash('Login successful', category='success')
                return redirect(url_for('home.index'))

        flash('Login failed. Please check your username and password.', category='error')

    return render_template("home/loginn.html")


@bp.route('/logout')
def logout():
# dit verwijderd de user_id van de session en logt de user uit
    session.pop('user_id', None)
    return redirect(url_for('home.index'))

@bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username1 = request.form.get('username')
# dit verwijderd elke character dat geen alphanummers zijn protecte tegen injections
        username  = ''.join(letter for letter in username1 if letter.isalnum())
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            hashed_password = sha256(password1.encode()).hexdigest()

            db = db_connection()  # Get the database connection
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (email, username, password) VALUES (%s, %s, %s)",
                           (email, username, hashed_password))
            db.commit()
            cursor.close()

            flash('Account Created!', category='success')
            return redirect(url_for('home.login'))

    return render_template("home/sign_up.html")

@bp.route("/about")
def about_me():
    return render_template("home/about.html")

@bp.route("/loginn")
def loggin_me():
    return render_template("home/loginn.html")
# ... Existing code ...

# ... Existing imports and code ...

@bp.route("/create_secret", methods=['GET', 'POST'])
def create_secret():
    if 'user_id' in session:
# 
        page1 = request.args.get('page', 1)
        page = int(re.sub('[^0-9]+', '', str(page1)))  # Convert to integer
        per_page = 10

# voor Dynamic website
        user_id = session['user_id']
        user = get_user_by_id(user_id)
        username = user['username']

# laatse login time
        last_login_time = get_last_login_time(user_id)

        if last_login_time:
            last_login_time = format_last_login_time(last_login_time)

        if request.method == 'POST':
# in de content vield voor protectie tegen injections
            content1 = request.form.get('content')
            content = ''.join(letter for letter in content1 if letter.isalnum())
# dit checkt dat de content input niet leeg is
            if content:
# insert secrets in de db
                user_id = session['user_id']
                db = db_connection()
                cursor = db.cursor()
                cursor.execute("INSERT INTO secrets (user_id, content) VALUES (%s, %s)", (user_id, content))
                db.commit()
                cursor.close()
                flash('Secret created successfully', category='success')
                return redirect(url_for('home.create_secret', page=page))
# dit laadt de secrets per pagina voor users
        user_id = session['user_id']
        secrets = get_user_secrets_paginated(user_id, page, per_page)

        return render_template("home/create_secret.html", secrets=secrets, page=page, per_page=per_page, username=username, last_login_time=last_login_time)

    return render_template("home/create_secret.html")


@bp.route("/edit_secret/<int:secret_id>", methods=['POST'])
def edit_secret(secret_id):
    if 'user_id' in session:
        user_id = session['user_id']
        new_content1 = request.form.get('new_content')
        new_content = ''.join(letter for letter in new_content1 if letter.isalnum())
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE secrets SET content = %s WHERE id = %s AND user_id = %s", (new_content, secret_id, user_id))
        db.commit()
        cursor.close()
        flash('Secret updated successfully', category='success')
        return redirect(url_for('home.create_secret'))

    return render_template("home/create_secret.html")

@bp.route("/delete_secret/<int:secret_id>", methods=['POST'])
def delete_secret(secret_id):
    if 'user_id' in session:
        user_id = session['user_id']
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM secrets WHERE id = %s AND user_id = %s", (secret_id, user_id))
        db.commit()
        cursor.close()
        flash('Secret deleted successfully', category='success')
        return redirect(url_for('home.create_secret'))

    return render_template("home/create_secret.html")


# Deze functie haalt een lijst op van gebruikersgeheimen op basis van de gebruikers-ID. Het voert een SELECT-query uit op de "secrets" tabel en retourneert een lijst van dictionaries met gegevens over de geheimen.
def get_user_secrets(user_id):
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM secrets WHERE user_id = %s", (user_id,))
    secrets_data = cursor.fetchall()
    cursor.close()

    secrets = [dict(zip(('id', 'user_id', 'content'), secret_data)) for secret_data in secrets_data]
        
    return secrets

# Vergelijkbaar met de vorige functie, haalt deze functie ook gebruikersgeheimen op, maar voegt een rijnummer toe aan elk geheim. Hiervoor wordt een SELECT-query met een rijnummer in SQL gebruikt.
def get_user_secrets2(user_id):
    db2 = db_connection()
    cursor2 = db2.cursor()
    cursor2.execute("SELECT (@cnt := @cnt + 1) AS rowNumber,t.content FROM secrets AS t CROSS JOIN (SELECT @cnt := 0) AS dummy WHERE user_id = %s", (user_id,))
    secrets_data2 = cursor2.fetchall()
    cursor2.close()

    secrets2 = [dict(zip(('id', 'user_id', 'content'), secret_data2)) for secret_data2 in secrets_data2]
        
    return secrets2





#  Deze functie haalt gebruikersinformatie op op basis van de gebruikers-ID. Het voert een SELECT-query uit op de "users" tabel en retourneert een dictionary met gebruikersdetails als de gebruiker wordt gevonden.
def get_user_by_id(user_id):
    db = db_connection()  # Get the database connection
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        user = dict(zip(('id', 'email', 'username', 'password'), user_data))
        return user
    return None



# Vergelijkbaar met de vorige functie, haalt deze functie gebruikersinformatie op op basis van de gebruikersnaam. Het doorzoekt de "users" tabel naar een overeenkomende gebruikersnaam en retourneert gebruikersgegevens als deze wordt gevonden.
def get_user_by_username(username):
    db = db_connection()  # Get the database connection
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        user = dict(zip(('id', 'email', 'username', 'password'), user_data))
        return user
    return None

# Deze functie haalt een gepagineerde lijst op van gebruikersgeheimen op basis van de gebruikers-ID, het paginanummer en het aantal items per pagina. Het gebruikt een SQL-query met LIMIT- en OFFSET-clausules om paginering te bereiken.
def get_user_secrets_paginated(user_id, page, per_page):
    db = db_connection()
    cursor = db.cursor()
    offset = (page - 1) * per_page
    cursor.execute("SELECT * FROM secrets WHERE user_id = %s LIMIT %s OFFSET %s", (user_id, per_page, offset))
    secrets_data = cursor.fetchall()
    cursor.close()

    secrets = [dict(zip(('id', 'user_id', 'content'), secret_data)) for secret_data in secrets_data]
        
    return secrets


# Deze functie haalt de laatste inlogtijd van een gebruiker op op basis van hun gebruikers-ID. Het voert een SELECT-query uit op de "users" tabel en retourneert de laatste inlogtijd als een opgemaakte tekenreeks.
def get_last_login_time(user_id):
    if 'user_id' in session and session['user_id'] == user_id:
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT last_login FROM users WHERE id = %s", (user_id,))
        last_login_time = cursor.fetchone()
        cursor.close()

        if last_login_time:
            return last_login_time[0]  # Directly return the last login time without converting

    return None


# Deze functie formatteert een laatste inlogtijd, (ontvangen als een datetime-object) tot een specifieke datum- en tijdsreeksindeling.
def format_last_login_time(last_login_time):
    if last_login_time is not None:
        formatted_time = last_login_time  # No need for conversion here
        return formatted_time.strftime("%Y-%m-%d %H:%M:%S")
    return None



if __name__ == "__main__":
    app = create_app()  # Create the Flask application
    app.run(debug=True)  # Start the development server with debugging enabled

