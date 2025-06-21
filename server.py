from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Respuestas predefinidas del chatbot
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
    "otra": "¡Gracias por tu mensaje! Por ahora solo puedo ayudarte con dudas sobre inscripción, contenidos, horarios y certificación.",
}

# Estado simple de sesión (global para ejemplo básico)
estado_sesion = {
    "esperando_inscripcion": False,
    "esperando_certificado": False,
}

# Middleware para permitir OPTIONS (preflight)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route("/api/chatbot", methods=['POST', 'OPTIONS'])
def chatbot():
    if request.method == 'OPTIONS':
        return '', 204

    if not request.is_json:
        return jsonify({"error": "Contenido no es JSON"}), 400

    data = request.get_json()
    pregunta = data.get("pregunta", "").lower().strip()

    # Respuesta según estado de sesión
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

# Inicia la app en entorno Railway o local
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
