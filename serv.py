from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import os
import json
import html
import re

baseFilePath = "index.html"


IMAGE_HEADER_TAG = "image/jpeg"
SONG_HEADER_TAG = "audio/mpeg"
JSON_HEADER_TAG = "application/json"

BASE = "C:/Users/B/Documents/GitHub/citron-presse/"



class Serv(BaseHTTPRequestHandler):
    global profile
    profile = 0
    
    def do_GET(self):

        parsed = self.path.split("/")[1:]
        print(parsed)
        if self.path == '/':
            self.path = '/' + baseFilePath

        elif self.path == "/icon.png":
            self.send_File_content("C:/Users/B/Documents/GitHub/citron-presse/icon.png", IMAGE_HEADER_TAG, hasHeader=False)
        elif self.path == "/song.mp3":
            self.send_File_content("C:/Users/B/Documents/GitHub/citron-presse/song.mp3", SONG_HEADER_TAG, hasHeader=False)
        elif re.match(r'/\d{2}-\d{2}-\d{4}\.mp3$', self.path):
            self.send_File_content(BASE + self.path[1:], parsed[0], hasHeader=False)
        elif self.path == "/lemon.jpg":
            self.send_File_content("C:/Users/B/Documents/GitHub/citron-presse/lemon.jpg", IMAGE_HEADER_TAG, hasHeader=False)
        elif self.path == "/favicon-32x32.png":
            self.send_File_content("C:/Users/B/Documents/GitHub/citron-presse/favicon-32x32.png", IMAGE_HEADER_TAG, hasHeader=False)



        try:
            file_to_open = open("C:/Users/B/Documents/GitHub/citron-presse/index.html").read()
            self.send_response(200)
        except:
            file_to_open = "File not found :&"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))










    def send_File_content(self, filePath: str, contentType: str, chunk_size=8192, hasHeader = True ):
        try:
            with open(filePath, "rb") as file:
                self.send_response(200)
                if hasHeader:
                    self.send_header('Content-type', contentType)
                self.end_headers()
                while chunk := file.read(chunk_size):
                    self.wfile.write(chunk)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

    def send_Json_content(self, jsonStr):
        self.send_response(200)
        self.send_header('Content-type', JSON_HEADER_TAG)
        self.end_headers()
        self.wfile.write(bytes(jsonStr, 'utf-8'))


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def run(server_class=ThreadedHTTPServer, handler_class=Serv, port=8080):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
