"""Baedge HTTP Server with API routes"""

import os
import logging

from flask import Flask, jsonify, make_response, request

# TODO: reenable
#import baedge

# application configuration
APP_NAME = "🎫 Baedge Server."
ROUTE_API_VERSION = "/v1"
ROUTE_NAMESPACE_DEVICE = "/device"
ROUTE_NAMESPACE_STATUS = "/status"
DEBUG_MODE = False
DOTENV = True
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# enable debug mode if log level is set to `DEBUG`
if LOG_LEVEL == "DEBUG":
    DEBUG_MODE = True

server_host = os.getenv("BAEDGE_SERVER_HOST", "0.0.0.0")
server_port = os.getenv("BAEDGE_SERVER_PORT", "2343")  # `2343` = `BDGE`

# load Flask framework
app = Flask(__name__)

@app.route("/", methods=['GET'])
def root_get():
    """ root endpoint """
    logging.debug("[root_get]")

    response = make_response(APP_NAME, 200)
    return response


@app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_STATUS, methods=['GET'])
def status_get():
    """ health endpoint """
    logging.debug("[status_get]")

    response = make_response("OK", 200)
    return response


@app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_STATUS + "/environment", methods=['GET'])
def status_environment_get():
    """ environment endpoint """
    logging.debug("[status_environment_get]")

    # iterate over environment variables and build a string
    environment_info = ""
    for key, value in os.environ.items():
        environment_info += f"{key}: {value}<br>"

    response = make_response(environment_info, 200)
    return response


@app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_STATUS + "/routes")
def status_routes_get():
    """ route status endpoint """
    logging.debug("[status_routes_get]")

    route_list = []
    for route in app.url_map.iter_rules():
        methods = ','.join(route.methods)
        route_list.append({
            'endpoint': route.endpoint,
            'methods': methods,
            'path': str(route),
       })

    response = make_response(jsonify(route_list), 200)
    return response


@app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_STATUS + "/screen", methods=['GET'])
def status_screen_get():
    """ screen status endpoint """
    logging.debug("[status_screen_get]")

    response = make_response("Device Status may be OK", 200)
    return response


@app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_DEVICE + "/clear", methods=['POST'])
def clear_post():
    """ screen-clearing endpoint """
    logging.debug("[clear_post]")

    #baedge.clear()

    # respond with status code and message
    response = make_response("OK", 200)
    return response


app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_DEVICE + "/write", methods=['POST'])
def write_post():
    """ screen-writing endpoint """
    logging.debug("[write_post] attempting to write to screen")

    # get data from request and parse as JSON
    data = request.get_json(force=True)

    if data.get('text'):
        #baedge.write_text(data.get('text'), data.get('style'))
        logging.debug("[write_post] writing text to screen")

        response = make_response("OK", 200)

    elif data.get('image'):
        #baedge.write_image(data.get('image'))
        logging.debug("[write_post] writing image to screen")

        response = make_response("OK", 200)

    else:
        logging.debug("[write_post] unable to write to screen")

        response = make_response("Payload did not contain expected data", 400)

    return response


# if no app name is specified, default to running Flask internally
if __name__ == "__main__":
    app.run(host=server_host, port=server_port, debug=DEBUG_MODE, load_dotenv=DOTENV)