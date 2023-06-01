from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import os

from src.classification import classificationExpense
from src.prediction import predictionExpense

app = Flask(__name__)
CORS(app)


@app.route('/api/classification/freq', methods=['POST'])
def classFreq():
    if (request.is_json):
        content = request.json

        nombre = content.get('freName', '')
        desc = content.get('freDescription', '')

        if (nombre == ''):
            return jsonify({'message': 'El nombre es obligatorio'}), 400
        if (desc == ''):
            return jsonify({'message': 'La descripcion es obligatoria'}), 400

        gasto_frecuente = nombre+" - "+desc

        classification = classificationExpense(gasto_frecuente)

        return jsonify({"message": 'Clasificacion obtenida correctamente', 'classification': classification}), 200

    return jsonify({'message': 'Peticion no valida'}), 400


@app.route('/api/classification/dia', methods=['POST'])
def classDia():
    if (request.is_json):
        content = request.json

        nombre = content.get('diaName', '')
        desc = content.get('diaDescription', '')

        print({"content": content})

        if (nombre == ''):
            return jsonify({'message': 'El nombre es obligatorio'}), 400
        if (desc == ''):
            return jsonify({'message': 'La descripcion es obligatoria'}), 400

        gasto_diario = nombre+" - "+desc

        # Clasificación

        classification = classificationExpense(gasto_diario)

        return jsonify({"message": 'Clasificacion obtenida correctamente', 'classification': classification, 'gasto': gasto_diario}), 200

    return jsonify({'message': 'Peticion no valida'}), 400


@app.route('/api/predictions', methods=['POST']) 
def predictGasto():
    if (request.is_json):
        content = request.json

        gastos = content.get('gastos', [])

        print({"content": content})

        if (gastos == []):
            return jsonify({'message': 'Los gastos son obligatorios'}), 400

        # Clasificación
        prediction = predictionExpense(gastos)

        return jsonify({"message": 'Predicción obtenida correctamente', 'prediction': prediction }), 200

    return jsonify({'message': 'Peticion no valida'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000), host='0.0.0.0')
