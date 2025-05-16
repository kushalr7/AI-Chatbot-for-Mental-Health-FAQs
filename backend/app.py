import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from model_utils import FAQMatcher
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Path to our FAQ CSV file
csv_path = os.path.join(os.path.dirname(__file__), 'data', 'faq.csv')

# Disclaimer message we'll attach to each response
DISCLAIMER = "Note: This is not medical advice. If you're struggling, please reach out to a licensed mental health professional or helpline."

# Create our FAQ matcher by loading the CSV and AI model
try:
    faq_matcher = FAQMatcher(csv_path)
    logger.info("FAQ Matcher initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize FAQ Matcher: {e}")
    faq_matcher = None

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/ask', methods=['POST'])
def ask():
    if faq_matcher is None:
        return jsonify({
            "response": "The service is currently unavailable. Please try again later.",
            "disclaimer": DISCLAIMER
        }), 503
    
    try:
        data = request.json
        if not data or 'query' not in data:
            return jsonify({
                "error": "No query provided",
                "disclaimer": DISCLAIMER
            }), 400
        
        query = data['query'].strip()
        if not query:
            return jsonify({
                "error": "Empty query provided",
                "disclaimer": DISCLAIMER
            }), 400
        
        answer, score, matched_question = faq_matcher.find_best_match(query)
        
        logger.info(f"Query processed with match score: {score:.4f}")
        
        return jsonify({
            "response": answer,
            "disclaimer": DISCLAIMER,
            "confidence": float(score),
            "matched_question": matched_question
        })
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({
            "error": "An error occurred while processing your request",
            "disclaimer": DISCLAIMER
        }), 500

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))
else:
    # For production
    # The app variable is used by gunicorn
    pass
