from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'LUMIS Embeddings Microservice',
        'message': 'Python Flask server is running!'
    })
if __name__ == '__main__':
    print("LUMIS Embeddings Service starting on http://localhost:8000")
    app.run(debug=True,port=8000,host='0.0.0.0')