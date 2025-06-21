from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Permitir acceso solo desde el frontend (ajusta si es necesario)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Respuestas predefinidas
respuestas = {
    "inscripcion_si": "¡Genial! Ya estás listo para comenzar. Revisa tu correo para los siguientes pasos.",
    "inscripcion_no": "Puedes inscribirte en el formulario oficial que te compartimos por correo o en la web del bootcamp.",
    "html": "El módulo de HTML cubre estructuras básicas, etiquetas, listas, formularios y más.",
    "css": "CSS Intermedio incluye selectores, flexbox, grid y responsive design.",
    "ia": "El módulo de IA introduce conceptos como Machine Learning, clasificación, clustering y más.",
    "presencial": "Los horarios presenciales son de lunes a viernes, 8am a 12pm.",
    "virtual": "Las sesiones virtuales son asincrónicas, con encuentros en vivo los miércoles a las 6pm.",
    "cert_si": "¡Felicitaciones! Estás listo para recibir tu certificado digital.",
    "cert_no": "Recuerda completar todos los módulos para poder certificarte.",
    "otra": "Lo siento, por ahora solo puedo ayudarte con dudas sobre inscripción, contenidos, horarios y certificación.",
}

# Estado simple por sesión (en producción deberías usar cookies o base de datos)
estado_sesion = {
    "esperando_inscripcion": False,
    "esperando_certificado": False,
}

# Middleware para añadir headers necesarios (opcional si CORS ya está configurado bien)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/api/chatbot", methods=['POST', 'OPTIONS'])
def chatbot():
    # Preflight CORS check
    if request.method == 'OPTIONS':
        return '', 204

    # Validar tipo de contenido
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json()
    pregunta = data.get("pregunta", "").lower().strip()

    # Lógica de flujo de conversación
    if estado_sesion["esperando_inscripcion"]:
        if pregunta in ["sí", "si", "ya me inscribí", "me inscribí"]:
            estado_sesion["esperando_inscripcion"] = False
            return jsonify({"respuesta": respuestas["inscripcion_si"]})
        elif pregunta == "no" or "no me he inscrito" in pregunta:
            estado_sesion["esperando_inscripcion"] = False
            return jsonify({"respuesta": respuestas["inscripcion_no"]})
        else:
            return jsonify({"respuesta": "Por favor responde con 'sí' o 'no'."})

    if estado_sesion["esperando_certificado"]:
        if pregunta in ["sí", "si", "ya terminé", "terminé"]:
            estado_sesion["esperando_certificado"] = False
            return jsonify({"respuesta": respuestas["cert_si"]})
        elif pregunta == "no" or "no he terminado" in pregunta:
            estado_sesion["esperando_certificado"] = False
            return jsonify({"respuesta": respuestas["cert_no"]})
        else:
            return jsonify({"respuesta": "Por favor responde con 'sí' o 'no'."})

    # Procesamiento general
    if "inscripción" in pregunta or "inscribirme" in pregunta or "inscribí" in pregunta:
        estado_sesion["esperando_inscripcion"] = True
        return jsonify({"respuesta": "¿Ya te inscribiste? Responde con 'sí' o 'no'."})

    elif "html" in pregunta:
        return jsonify({"respuesta": respuestas["html"]})

    elif "css" in pregunta:
        return jsonify({"respuesta": respuestas["css"]})

    elif "inteligencia artificial" in pregunta or "ia" in pregunta:
        return jsonify({"respuesta": respuestas["ia"]})

    elif "presencial" in pregunta:
        return jsonify({"respuesta": respuestas["presencial"]})

    elif "virtual" in pregunta:
        return jsonify({"respuesta": respuestas["virtual"]})

    elif "certificado" in pregunta or "certificación" in pregunta:
        estado_sesion["esperando_certificado"] = True
        return jsonify({"respuesta": "¿Terminaste todos los módulos? Responde con 'sí' o 'no'."})

    else:
        return jsonify({"respuesta": respuestas["otra"]})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
