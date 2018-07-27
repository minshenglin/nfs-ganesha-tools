from flask import Flask
from flask import jsonify
from ceph import CephHandler
from ganesha import GaneshaConfig

app = Flask(__name__)
#app.run(port=8080, debug=True)

@app.route('/api/v1.0/nfs/config', methods=['GET'])
def get_task():
    ceph_handler = CephHandler()
    content = ceph_handler.read("nfs-ganesha", "export")
    config = GaneshaConfig.parser(content) 
    return jsonify(config.dict())
