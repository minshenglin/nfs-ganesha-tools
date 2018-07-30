from flask import Flask
from flask import jsonify
from flask import request
from ceph import CephHandler
from ganesha import GaneshaConfig

app = Flask(__name__)
#app.run(port=8080, debug=True)

@app.route('/api/v1.0/nfs/config', methods=['GET'])
def get_config():
    ceph_handler = CephHandler()
    content = ceph_handler.read("nfs-ganesha", "export")
    config = GaneshaConfig.parser(content) 
    return jsonify(config.dict())

@app.route('/api/v1.0/nfs/config', methods=['PUT'])
def update_confg():
    if not request.json:
        abort(400)
    
    ceph_handler = CephHandler()
    if 'export' not in request.get_json():
        abort(400)

    config = GaneshaConfig.parserJson(request.json)
    ceph_handler.write("nfs-ganesha", "export", str(config))
    return jsonify(config.dict())
