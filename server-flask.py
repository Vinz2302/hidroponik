from flask import Flask, request, jsonify
from firebaseConn import generate_download_url
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/arduino', methods=['GET'])
def test_arduino():
    from action.instruction import arduino_control
    arduino_control()
    return jsonify({'message': 'Success'})

@app.route('/image', methods=['POST'])
def get_download_url_post():
    # Get the file_path from the body
    data = request.get_json()

    if 'file_path' not in data:
        return jsonify({'error': 'File path not provided'}), 400

    file_path = data['file_path']
    download_url = generate_download_url(file_path)

    return jsonify({'download_url': download_url})

@app.route('/image', methods=['GET'])
def get_download_url():
    #Get the file_path from the param
    file_path = request.args.get('file_path')

    if not file_path:
        return jsonify({'error': 'File path not provided in query parameter'}), 400
    
    download_url = generate_download_url(file_path)
    return jsonify({'download_url': download_url})


if __name__ == '__main__':
    app.run(port=8000)