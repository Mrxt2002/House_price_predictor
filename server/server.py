from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        locations = util.get_location_names()
        response = jsonify({'locations': locations})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        data = request.form
        total_sqft = data.get('total_sqft', None)
        location = data.get('location', None)
        bhk = data.get('bhk', None)
        bath = data.get('bath', None)

        if not total_sqft or not location or not bhk or not bath:
            return jsonify({'error': 'Invalid input parameters'}), 400
        
        total_sqft = float(total_sqft)
        bhk = int(bhk)
        bath = int(bath)

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({'estimated_price': estimated_price})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except ValueError:
        return jsonify({'error': 'Invalid data type for total_sqft, bhk, or bath'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    try:
        print("Starting Python flask server for Home price prediction")
        util.load_saved_artifacts()
        app.run()
    except Exception as e:
        print(f"Error starting server: {e}")
