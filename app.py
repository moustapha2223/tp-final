from flask import Flask, request, jsonify
from ultralytics import YOLO
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Charger le modèle YOLO
model = YOLO("best.pt")

def extract_predictions(predictions):
    # Extrait les informations des prédictions et les formate en un dictionnaire JSON serializable
    results = []
    for pred in predictions[0]:
        label = pred['label']
        confidence = pred['confidence']
        bbox = pred['bbox']
        results.append({
            "label": label,
            "confidence": confidence,
            "bbox": bbox
        })
    return results

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Vérifie si une image a été envoyée
        if 'file' not in request.files:
            return jsonify({"error": "Aucune image n'a été envoyée."}), 400

        # Récupère l'image depuis la requête
        file = request.files['file']

        # Vérifie si le fichier est une image
        if file.filename == '':
            return jsonify({"error": "Nom de fichier vide."}), 400

        if not file.content_type.startswith('image/'):
            return jsonify({"error": "Le fichier n'est pas une image valide."}), 400

        # Charge l'image depuis les octets      
        image_bytes = BytesIO(file.read())
        img = Image.open(image_bytes)

        # Effectue la prédiction
        results = model(img)

        # Extrait les prédictions et les renvoie au format JSON
        extracted_results = extract_predictions(results)
        return jsonify(extracted_results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
