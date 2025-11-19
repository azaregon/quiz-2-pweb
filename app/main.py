import flask
from flask_bcrypt import Bcrypt
from .controllers.coba_controllers import coba_bp
from .controllers.auth_controllers import auth_bp
from .controllers.project_controllers import project_bp


app = flask.Flask(__name__)
# app.config['APPLICATION_ROOT'] = '/api'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.register_blueprint(coba_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(project_bp)

# ----------------------------------- login-system ---------------------------------- #
# @app.route("/login")


if __name__ == '__main__':
    app.run(debug=True)