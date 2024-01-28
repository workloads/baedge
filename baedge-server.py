from flask import Flask,request
import baedge

#app = init_app()

app = Flask(__name__)


@app.route("/v1/health")
def status():
    return "OK"

@app.route("/v1/status")
def hello_world():
    return "e-ink device status maybe OK>"

@app.route("/v1/clear", methods=['POST'])
def clear():
    baedge.clear()
    return "Cleared"

@app.route("/v1/write", methods=['POST'])
def write():
    data = request.get_json(force=True)
    if data.get('text'):
        baedge.write_text(data.get('text'), data.get('style'))
    elif data.get('image'):
        baedge.write_image(data.get('image'))
    else:
        return "One of image or data need to be declared", 400
    return "Successfully wrote to e-ink device"
