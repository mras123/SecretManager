import secrets
from flask import Flask
import secretsapp.home
import secretsapp.db as db
from flask_login import LoginManager

def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SECRET_KEY"] = secrets.token_hex(64)

    
    login_manager = LoginManager()
    login_manager.login_view = "home.login"
    login_manager.init_app(app)

    from secretsapp.home import get_user_by_id 

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)

   
    app.teardown_appcontext(db.teardown_db)

   
    app.register_blueprint(secretsapp.home.bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
