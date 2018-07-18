#####################
# Application Setup #
#####################

import logging

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_openid import OpenID
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
CORS(app)
oid = OpenID(app, store_factory=lambda: None)
migrate = Migrate(app, db)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per minute"]
)


##########
# Routes #
##########

@app.route('/docs/<path:path>')
def access_docs(path):
    return send_from_directory('docs', path)

from routes.user import build_api_user
from routes.auth import build_api_auth
from routes.game import build_api_game
from routes.community import build_api_community
from routes.stream_system import build_api_stream_system

build_api_auth(app, oid)
build_api_user(app)
build_api_game(app)
build_api_community(app)
build_api_stream_system(app)

########################
# Default Error Routes #
########################

@app.errorhandler(400)
def unauthorized(e):
    return jsonify({'success': 'no',
                    'error': 'HTTP400-InvalidRequest',
                    'payload': {}}), 200


@app.errorhandler(401)
def unauthorized(e):
    return jsonify({'success': 'no',
                    'error': 'HTTP401-AuthorizationError',
                    'payload': {}}), 200

@app.errorhandler(404)
def unknown(e):
    return jsonify({'success': 'no',
                    'error': 'HTTP404-UnknownEndpoint',
                    'payload': {}}), 200

@app.errorhandler(405)
def unknown(e):
    return jsonify({'success': 'no',
                    'error': 'HTTP405-WrongMethodOnEndpoint',
                    'payload': {}}), 200

@app.errorhandler(429)
def rate_limit_handler(e):
    return jsonify({'success': 'no',
                    'error': 'HTTP429-RequestRateLimit',
                    'payload': {}}), 200

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
