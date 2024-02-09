import json
import os
import flask
from vrchat_oscquery.threaded import vrc_osc
from vrchat_oscquery.common import vrc_client, dict_to_dispatcher

configData = [{}]
app = flask.Flask(__name__)
client = vrc_client()

@app.route("/")
def main():
    print("Sending index.html")
    return flask.send_file("index.html")

@app.route("/config.json")
def sendConfig():
    print("Sending config", configData)
    return configData[0]

@app.route("/osc")
def osc():
    b = flask.request.args.get('bool')
    if b:
        client.send_message(flask.request.args.get('addr'), b != "0")
        return "send %s" % (b!="0")
    f = flask.request.args.get('float')
    if f:
        client.send_message(flask.request.args.get('addr'), float(f))
        return "send %s" % float(f)
    s = flask.request.args.get('str')
    if s:
        client.send_message(flask.request.args.get('addr'), s)
        return "send %s" % s
    return "err"
    
def avatar_changed(path, id):
    print("avatar ", id)
    p = os.path.expandvars("%appdata%\\..\\LocalLow\\VRChat\\VRChat\\OSC")
    found_at = None
    for cur, folders, files in os.walk(p):
        if id+".json" in files:
            found_at = os.path.join(cur, id + ".json")
    if not found_at:
        print("Couldn't find osc json file.")
        configData[0]={}
    else:
        with open(found_at, "rb") as config:
            print("Loaded", found_at)
            configData[0]=json.loads(config.read())
            

if __name__ == "__main__":
    vrc_osc("VarServer", dict_to_dispatcher({
        "/avatar/change": avatar_changed
    }), foreground=False)
    app.run(host="0.0.0.0", use_reloader=False)
