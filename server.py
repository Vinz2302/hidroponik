# import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
import sys
import signal
from firebaseConn import generate_download_url

PORT = 8000

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        # self.send_header('Content_type', 'application/json')
        self.send_header('Content_type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if 'file_path' not in data:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'File path not provided'}).encode('utf-8'))
            return
        
        file_path = data['file_path']
        download_url = generate_download_url(file_path)

        self._set_headers()
        response = {'download_url': download_url}
        self.wfile.write(json.dumps(response).encode('utf-8'))

def signal_handler(sig, frame):
    print('Exiting...')
    sys.exit(0)

def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {PORT}')

    signal.signal(signal.SIGINT, signal_handler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print('Server Closed')

if __name__ == '__main__':
    run()