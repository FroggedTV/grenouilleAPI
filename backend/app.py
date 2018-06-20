#####################
# Application Setup #
#####################

from flask import Flask, jsonify, send_from_directory
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
oid = OpenID(app, store_factory=lambda: None)
migrate = Migrate(app, db)

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
