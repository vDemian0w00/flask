from flask import Flask, jsonify, request
import os

app = Flask(__name__)


@app.route('/api/test', methods=['POST'])
def test():
    if (request.is_json):
        content = request.json
        print(content)
        return jsonify({"Choo Choo": content}), 200

    return jsonify({'message': 'Peticion no valida'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
