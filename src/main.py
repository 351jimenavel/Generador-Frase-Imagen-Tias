import os
import requests
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
NOVITA_API_KEY = os.getenv("sk_wM9mak8V8vJsL7foCG6WTNSJpahzqPQ-swNPsCfsSDo")

app = Flask(__name__)
CORS(app)

ESTILOS_IMAGENES = {
    "piolin": [
        "https://images.app.goo.gl/q6m3WXN5kA7fkk4y8",
        "https://images.app.goo.gl/QU6pD7VwWserCVkb6",
        "https://images.app.goo.gl/bFCQR1eeitwqirrDA"
    ],
    "flores": [
        "https://images.app.goo.gl/FQzMcM1Q9fhSxxRP7",
        "https://images.app.goo.gl/T37c9tckh9RhmVjR8",
        "https://images.app.goo.gl/cfLjqPhVDDsSSaGC6"
    ],
    "animales": [
        "https://images.app.goo.gl/915Mk7bfQPnAYzpV6",
        "https://images.app.goo.gl/N2xCPwtBf4s3mMpn8",
        "https://images.app.goo.gl/6nLmxhwugo9KsHx67"
    ]
}

@app.route('/generar', methods=['POST'])
def generar():
    data = request.json
    frase = data.get("frase")
    estilo = data.get("estilo")

    if not frase or not estilo:
        return jsonify({"error": "Faltan parámetros 'frase' o 'estilo'"}), 400

    urls = ESTILOS_IMAGENES.get(estilo.lower())
    if not urls:
        return jsonify({"error": f"Estilo '{estilo}' no soportado"}), 400

    url_imagen = random.choice(urls)

    headers = {
        "Authorization": f"Bearer {NOVITA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": frase,
        "image_url": url_imagen,
    }

    response = requests.post(
        "https://api.novita.io/v1/generate",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return jsonify({"error": "Error al generar imagen con Novita", "details": response.text}), 500

    resultado = response.json()
    imagen_base64 = resultado.get("image_base64")
    if not imagen_base64:
        return jsonify({"error": "No se recibió imagen de Novita"}), 500

    return jsonify({
        "mensaje": "Imagen generada con éxito",
        "imagen_base64": imagen_base64
    })

@app.route('/')
def home():
    return jsonify({"msg": "Backend Novita listo y escuchando 🧠✨"})

if __name__ == "__main__":
    app.run(debug=True)