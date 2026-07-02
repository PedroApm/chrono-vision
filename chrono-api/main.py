from flask import Flask, jsonify, request
import random
from datetime import datetime
import requests

app = Flask(__name__)

def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.after_request
def after_request(response):
    return add_cors(response)

@app.route('/procesar')
def procesar():
    id_edificio = request.args.get('id', 'desconocido')
    return jsonify({
        'id': id_edificio,
        'procesado': True,
        'timestamp': datetime.utcnow().isoformat(),
        'nivel_dano': random.randint(60, 95),
        'era': 'Pre-Colapso 2077',
        'fragmentos_recuperados': random.randint(3, 12),
        'mensaje': 'Procesamiento completado en servidor'
    })

@app.route('/analizar-imagen', methods=['POST', 'OPTIONS'])
def analizar_imagen():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json()
    imagen_b64 = data.get('imagen', '')
    ## GEMINI_KEY = ''
    ##url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}'

    payload = {
        'contents': [{
            'parts': [
                {'text': 'Identifica brevemente este lugar o monumento. Responde solo con: LUGAR: [nombre], HISTORIA: [2 oraciones maximas], AÑO: [año aproximado de construccion]. Si no es un lugar reconocible responde: NO RECONOCIDO.'},
                {'inline_data': {'mime_type': 'image/jpeg', 'data': imagen_b64}}
            ]
        }],
        'generationConfig': {'maxOutputTokens': 150}
    }

    resp = requests.post(url, json=payload)
    resultado = resp.json()
    if 'candidates' in resultado:
        texto = resultado['candidates'][0]['content']['parts'][0]['text']
    elif 'error' in resultado:
        texto = 'ERROR GEMINI: ' + resultado['error'].get('message', 'desconocido')
    else:
        texto = 'RESPUESTA INESPERADA: ' + str(resultado)

    return jsonify({'respuesta': texto})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
