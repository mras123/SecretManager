import secrets
from flask import Flask
import secretsapp.home
import secretsapp.db as db
# dit is een functie in flask voor session manegment.
from flask_login import LoginManager
# dit maakt de flask app
def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SECRET_KEY"] = secrets.token_hex(64)

# Initialize Flask-Login 
    login_manager = LoginManager()
# als een user wilt inlogged worden ze geriderct naar hoar home.login view
    login_manager.login_view = "home.login"
# maakt connectie met de flask app
    login_manager.init_app(app)

    # Define the user loader function
    from secretsapp.home import get_user_by_id  # Import the function from home.py
# dit verteld flask-login hoe het een user bij zin id moet laden
    @login_manager.user_loader
# dit laat de user gebaseerd op zijn ID en gebruikt de get_user_by_id functie bij de home module
    def load_user(user_id):
        return get_user_by_id(user_id)

    # Register a teardown function for cleaning up the database connection
    app.teardown_appcontext(db.teardown_db)

    # Register the 'secretsapp.home' blueprint for handling routes
    app.register_blueprint(secretsapp.home.bp)

    return app
# kijkt of de script runt als de main programma 
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
