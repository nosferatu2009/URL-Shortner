import random
import logging
import string
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

data_store = {}
BASE_URL = "https://localhost:5001/"

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


@app.route("/shorten", methods=["POST"])
def shorten_url():
    try:
        
        data = request.json
        long_url = data.get('long_url')

        if not long_url :
            return jsonify({ "error" : "url not found!"}), 400
        for short, long in data_store.items() :
            if long == long_url :
                return jsonify({"short url" : BASE_URL + short})
        
        short_url = generate_short_url()
        data_store[short_url] = long_url

        return jsonify({"short url" : BASE_URL + short_url})
    except Exception as ex :
        logging.error(f'error {ex}')
        return jsonify({"error" : "Internal Server Error"}), 500 


@app.route('/<short_url>', methods=["GET"])
def redirect_url(short_url):
    try:
        long_url = data_store.get(short_url)

        if not long_url:
            return jsonify({"error" : "url not found"}), 404
        else:
            return jsonify({"long url" : long_url})
    except Exception as ex:
        logging.error(f'error {ex}')
        return jsonify({"error" : "Internal Server Error"}), 500     
    

if __name__ == "__main__" :
    app.run(debug=True)


