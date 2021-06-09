from flask import Flask
from . import error_pages

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        TEMPLATES_AUTO_RELOAD=True,
    )
    
    # register a 404 page
    app.register_error_handler(404, error_pages.page_not_found)
    
    from .database_extensions import init_database_extensions, verify_db_state
    init_database_extensions(app)
    verify_db_state()

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for edit parts of app
    from .edit import edit as edit_blueprint
    app.register_blueprint(edit_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
