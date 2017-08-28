#####################
# Application Setup #
#####################

from flask import Flask, jsonify
from flask_migrate import Migrate

from cfg.configuration import load_config
from models import db


def create_app():
    """Factory to create the Flask application with cfg and db."""
    app = Flask(__name__)
    load_config(app.config)
    db.init_app(app)
    return app

app = create_app()
migrate = Migrate(app, db)

##########
# Routes #
##########

from routes.user import build_api_user

build_api_user(app)

########################
# Default Error Routes #
########################

@app.errorhandler(401)
def unauthorized(e):
    return jsonify({'success': 'no',
                    'error': 'Authorization error.',
                    'payload': {}}), 401

@app.errorhandler(404)
def unknown(e):
    return jsonify({'success': 'no',
                    'error': 'Unknown endpoint.',
                    'payload': {}}), 404

############################
# Start Tornado Web Server #
############################

if __name__ == "__main__":
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    server = HTTPServer(WSGIContainer(app))
    server.bind(address='0.0.0.0', port=int(app.config['PORT']))
    server.start(0)  # Forks multiple sub-processes
    IOLoop.current().start()
