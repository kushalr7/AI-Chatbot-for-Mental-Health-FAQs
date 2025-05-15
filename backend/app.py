from flask import Flask, request, jsonify
from flask_cors import CORS
from model_utils import FAQMatcher
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Path to the FAQ CSV file
csv_path = os.path.join(os.path.dirname(__file__), 'data', 'faq.csv')

# Disclaimer message
DISCLAIMER = "Note: This is not medical advice. If you're struggling, please reach out to a licensed mental health professional or helpline."

# Initialize the FAQ matcher
try:
    faq_matcher = FAQMatcher(csv_path)
    logger.info("FAQ Matcher initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize FAQ Matcher: {e}")
    faq_matcher = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the server is running."""
    return jsonify({"status": "healthy"})

@app.route('/ask', methods=['POST'])
def ask():
    """
    Endpoint to ask a question to the FAQ system.
    
    Expected JSON body: {"query": "user question here"}
    Returns: {"response": "answer text", "disclaimer": "disclaimer text"}
    """
    if faq_matcher is None:
        return jsonify({
            "response": "The service is currently unavailable. Please try again later.",
            "disclaimer": DISCLAIMER
        }), 503
    
    try:
        # Get the query from the request
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
        
        # Find the best matching answer
        answer, score, matched_question = faq_matcher.find_best_match(query)
        
        # Log the interaction (but don't store user data)
        logger.info(f"Query processed with match score: {score:.4f}")
        
        # Return the answer with disclaimer
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
    app.run(debug=True, host='0.0.0.0', port=5000)

# Future improvements:
# 1. Add multiple language support by incorporating language detection and translation
# 2. Integrate generative models (like GPT) for questions outside the FAQ scope
# 3. Add authentication for admin-only features like FAQ management
# 4. Implement rate limiting to prevent abuse
# 5. Add a feedback mechanism to improve answers over time
