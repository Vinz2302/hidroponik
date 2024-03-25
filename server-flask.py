from flask import Flask, request, jsonify
# from firebaseConn import generate_download_url
from flask_cors import CORS
from routes.image import image_routes

PORT = 8000

app = Flask(__name__)
CORS(app)

@app.route('/arduino', methods=['GET'])
def test_arduino():
    from action.instruction import arduino_control
    arduino_control()
    return jsonify({'message': 'Success'})

app.register_blueprint(image_routes)

if __name__ == '__main__':
    app.run(port=PORT)