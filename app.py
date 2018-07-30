from flask import Flask
from flask import jsonify
from flask import request
from ceph import CephHandler
from ganesha import GaneshaConfig
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

@app.route('/api/v1.0/nfs/config', methods=['GET'])
@auth.login_required
def get_config():
    ceph_handler = CephHandler()
    content = ceph_handler.read("nfs-ganesha", "export")
    config = GaneshaConfig.parser(content) 
    return jsonify(config.dict())

@app.route('/api/v1.0/nfs/config', methods=['PUT'])
@auth.login_required
def update_confg():
    if not request.json:
        abort(400)
    
    ceph_handler = CephHandler()
    if 'export' not in request.get_json():
        abort(400)

    config = GaneshaConfig.parserJson(request.json)
    ceph_handler.write("nfs-ganesha", "export", str(config))
    return jsonify(config.dict())

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False

    usr = ceph_handler.read("nfs-ganesha", "username")
    pw = ceph_handler.read("nfs-ganesha", "password")

    return username == usr and password == pw

if __name__ == '__main__':
    ceph_handler = CephHandler()
    ceph_handler.write("nfs-ganesha", "username", "admin")
    ceph_handler.write("nfs-ganesha", "password", "password")
    app.run(host='192.168.15.100', port=5000, debug=True)
