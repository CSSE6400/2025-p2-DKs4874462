from flask import Flask
from flask_sqlalchemy import SQLAlchemy
def create_app(config_overrides):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
    if config_overrides:
        app.config.update(config_overrides)

    from todo.models import db
    from todo.models.todo import Todo
    db.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()
    
    from todo.views.routes import api
    app.register_blueprint(api)

    return app
