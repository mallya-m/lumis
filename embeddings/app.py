from flask import Flask, request,jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import os
import time

load_dotenv()

app = Flask(__name__)

CORS(app)

print("Loading sentence-transformer model...")
start = time.time()

model = SentenceTransformer(
    'all-MiniLM-L6-v2',
    cache_folder='./models'
)
print(f"Model loaded in {time.time() - start:.2f}s")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model': 'all-MiniLM-L6-v2',
        'vector_dimensions': 384
    })

@app.route('/embed', methods=['POST'])
def embed():
    """
    Takes text → returns a 384-number vector

    Request body (JSON):
    { "text": "flowy dress for beach wedding" }

    Response (JSON):
    { "embedding": [0.123, -0.456, 0.789, ... 384 numbers total] }

    Simple explanation:
    Imagine each word has a "location" in a 384-dimensional space
    (we can't visualize 384 dimensions but the math works the same as 2D or 3D)
    The model finds the "average location" of all the words in your sentence
    Similar sentences end up near each other in this space
    We use this to find products that are "near" the user's search query

    Technical explanation:
    The model encodes input text using a fine-tuned BERT architecture,
    mean-pooling the token embeddings to produce a fixed-size 384-dimensional
    dense vector. Cosine similarity between two vectors measures semantic
    relatedness — values near 1.0 = very similar, near 0 = unrelated.
    """

    # Get the JSON body from the request
    data = request.get_json()

    # Validate: make sure 'text' field exists and isn't empty
    if not data or 'text' not in data or not data['text'].strip():
        # 400 = "Bad Request" — client sent something we can't work with
        return jsonify({'error': 'text field is required'}), 400

    text = data['text'].strip()

    # model.encode() is the magic:
    # Takes a string → runs it through the neural network → returns 384 numbers
    # convert_to_list=True converts numpy array to plain Python list
    # (we need plain list to convert to JSON — numpy arrays aren't JSON serializable)
    embedding = model.encode(text).tolist()

    return jsonify({
        'embedding': embedding,
        'dimensions': len(embedding),  # should always be 384
        'text': text                   # echo back so caller can verify
    })


@app.route('/embed-batch', methods=['POST'])
def embed_batch():
    
    data = request.get_json()

    if not data or 'texts' not in data or not isinstance(data['texts'], list):
        return jsonify({'error': 'texts array is required'}), 400

    texts = [t.strip() for t in data['texts'] if t.strip()]

    if len(texts) == 0:
        return jsonify({'error': 'texts array cannot be empty'}), 400

    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    
    return jsonify({
        'embeddings': embeddings,       # list of 384-number lists
        'count': len(embeddings),
        'dimensions': 384
    })


if __name__ == '__main__':
    print("Starting LUMIS Embeddings Service on http://localhost:8000")
    app.run(debug=True, port=8000, host='0.0.0.0')
