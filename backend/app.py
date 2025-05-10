from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

# logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
app = Flask(__name__)
CORS(app)

# OpenAI client with Together AI base URL
api_key = os.getenv("TOGETHER_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("No API key found in environment variables")
    raise ValueError("API key not found! Check your .env file")

logger.info(f"Using API base URL: https://api.together.xyz/v1")
logger.info(f"API Key (first 4 chars): {api_key[:4]}..." if api_key else "No API key!")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.together.xyz/v1"
)

@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        logger.info("Received request to /api/analyze")
        data = request.get_json()
        logger.debug(f"Request data: {data}")
        
        if not data:
            logger.warning("No data provided in request")
            return jsonify({"error": "No data provided"}), 400
            
        text = data.get("text", "")
        if not text:
            logger.warning("No text provided in request data")
            return jsonify({"error": "No text provided"}), 400

        logger.info(f"Processing text: '{text}'")
        prompt = f"Given this text: \"{text}\", suggest 2-3 related search queries or questions."

        logger.info(f"Sending request to Together AI API with model: mistral-7b-instruct")
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content.strip()
        logger.info(f"Received response from API: '{result[:50]}...'")
        return jsonify({"result": result})
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/test", methods=["GET"])
def test():
    """Simple test endpoint to verify the API is working"""
    return jsonify({"status": "API is working!"})

if __name__ == "__main__":
    logger.info("Starting Flask server...")
    app.run(debug=True)