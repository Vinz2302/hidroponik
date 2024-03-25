from flask import Blueprint, request, jsonify
from firebaseConn import generate_download_url, upload_image

image_routes = Blueprint('image', __name__)

@image_routes.route('/image', methods=['POST'])
def get_image_post():
    data = request.get_json()
    if 'file_path' not in data:
        return jsonify({'error': 'File path not provided'}), 400
    
    file_path = data['file_path']
    download_url = generate_download_url(file_path)
    return jsonify({'download_url': download_url})

@image_routes.route('/image', methods=['GET'])
def get_image():
    file_path = request.args.get('file_path')
    if not file_path:
        return jsonify({'error': 'File path not provided in query param'}), 400
    
    upload_image('image/pameran.jpg', 'test1/pameran.jpg')
    
    download_url = generate_download_url(file_path)
    return jsonify({'download_url': download_url})