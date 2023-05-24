from flask import Flask, json, request, jsonify

class App():
  
  app = Flask(__name__)

  @app.route('/api/<id>', methods=['GET'])
  def hello_world(id):
    return jsonify({'id': id})
  
  def createApp(self):
    self.app.run(host='0.0.0.0', port=5000, debug=True)
    print('App running on port 5000')