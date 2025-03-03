from flask import Flask
from flask_sqlalchemy import SQLAlchemy
def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"

    from todo.models import db
    from todo.models.todo import Todo
    db.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()
    
    from todo.views.routes import api
    app.register_blueprint(api)

    return app
