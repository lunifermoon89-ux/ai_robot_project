from flask import Flask, request, jsonify, send_from_directory
from predict_traffic_i import predict_value, load_model, MODEL_FILE
import logging
import json
import os
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ai_robot_project')

# Load model once at startup to avoid repeated disk I/O
try:
    MODEL = load_model(MODEL_FILE)
    logger.info('Model loaded at startup')
except Exception:
    MODEL = None
    logger.warning('Model not loaded at startup')

# Prometheus metrics
PREDICTIONS = Counter('ai_robot_project_predictions_total', 'Total number of predictions')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model_loaded': MODEL is not None})


@app.route('/ready', methods=['GET'])
def ready():
    # readiness: ensure model is loadable
    try:
        _ = load_model(MODEL_FILE)
        return jsonify({'ready': True})
    except Exception:
        return jsonify({'ready': False}), 503


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json() or {}
    if 'X_Feature' not in data:
        return jsonify({'error': "request JSON must include 'X_Feature'"}), 400

    try:
        value = float(data['X_Feature'])
    except Exception:
        return jsonify({'error': 'X_Feature must be numeric'}), 400

    # Lazy-load model if not present (helps tests that train the model at runtime)
    global MODEL
    if MODEL is None:
        try:
            MODEL = load_model(MODEL_FILE)
        except FileNotFoundError:
            logger.exception('Model file not found')
            return jsonify({'error': 'model file not found'}), 500
        except Exception as e:
            logger.exception('Error loading model')
            return jsonify({'error': str(e)}), 500

    try:
        score = predict_value(value)
        PREDICTIONS.inc()
        logger.info('Predicted score for %s: %s', value, score)
        return jsonify({'input': value, 'predicted_traffic_score': score})
    except Exception as e:
        logger.exception('Prediction error')
        return jsonify({'error': str(e)}), 500


@app.route('/metrics')
def metrics():
    # Expose Prometheus metrics
    data = generate_latest()
    return (data, 200, {'Content-Type': CONTENT_TYPE_LATEST})


@app.route('/openapi.json', methods=['GET'])
def openapi():
    # Minimal OpenAPI spec for the service
    spec = {
        'openapi': '3.0.0',
        'info': {'title': 'ai_robot_project API', 'version': '1.0'},
        'paths': {
            '/predict': {
                'post': {
                    'summary': 'Predict traffic score',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {'type': 'object', 'properties': {'X_Feature': {'type': 'number'}}}
                            }
                        }
                    },
                    'responses': {
                        '200': {'description': 'Prediction', 'content': {'application/json': {}}},
                        '400': {'description': 'Bad Request'},
                        '500': {'description': 'Server Error'},
                    },
                }
            },
            '/health': {'get': {'summary': 'Health check'}},
            '/ready': {'get': {'summary': 'Readiness check'}},
        },
    }
    return jsonify(spec)


@app.route('/docs')
def docs():
    # Serve a minimal Swagger UI that loads /openapi.json from CDN
    html = '''<!doctype html>
<html>
  <head>
    <title>ai_robot_project API docs</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@4/swagger-ui.css" />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@4/swagger-ui-bundle.js"></script>
    <script>
      window.ui = SwaggerUIBundle({
        url: '/openapi.json',
        dom_id: '#swagger-ui',
      })
    </script>
  </body>
</html>'''
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
