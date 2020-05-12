from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from gtts import gTTS 
import os 
import tempfile
import urllib.parse
#<form action='/send' method='post'><h2>Send Message</h2><input type='text' name='message'></input><input type='submit' value='submit'></input> </form>
#setup for text to speech and printing
language = 'en'
filename = tempfile.mktemp(".txt")

with open('index.html', 'r') as f:
    html_string = f.read()

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write(html_string.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode())
        
        data = post_data.decode("utf-8")
        data = urllib.parse.unquote(data)
        data = data.split('message=')
        data = data[1]
        data = data.replace('+', ' ')
        print(data)


        #print message
        open (filename , "w").write (data)
        os.startfile(filename, "print")
        
        #text to speech 
        myobj = gTTS(text=data, lang=language, slow=False)
        myobj.save("message.mp3") 
        os.system("start message.mp3") 
         
        
        self._set_response()
        self.wfile.write("Message Sent".encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
