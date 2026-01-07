import http.server
import socketserver
import urllib.parse
import qrcode
import webbrowser
import sys
import socket
import threading
import io

PORT = 8000

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def print_qr(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Launch Chrome</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; background-color: #f0f0f0; }
                form { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); display: flex; flex-direction: column; gap: 10px; width: 300px; }
                input { padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; }
                button { padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }
                button:hover { background-color: #0056b3; }
            </style>
        </head>
        <body>
            <form action="/launch" method="post">
                <h2 style="text-align: center; margin-top: 0;">Launch Chrome</h2>
                <input type="text" name="url" placeholder="Enter URL (e.g. google.com)" required>
                <button type="submit">Send</button>
            </form>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        if self.path == '/launch':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))
            url = params.get('url', [''])[0]
            
            if url:
                if not url.startswith('http://') and not url.startswith('https://'):
                    url = 'https://' + url
                
                print(f"Launching Chrome with URL: {url}")
                
                # Try to find chrome specifically
                try:
                    # Windows specific chrome path check or generic open
                    # 'google-chrome' might be registered, or just use default if it's chrome.
                    # Given the user request "launch chrome", we should try to be specific if possible.
                    # But webbrowser.get('chrome') often fails on Windows if not registered exactly so.
                    # We will try 'google-chrome' then fall back to default if that fails, 
                    # but usually just webbrowser.open(url) uses default. 
                    # If we MUST open chrome specifically and it's not default:
                    
                    # Common windows path
                    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                    chrome_path_x86 = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                    
                    browser = None
                    if 'chrome' in webbrowser._browsers:
                         browser = webbrowser.get('chrome')
                    elif 'google-chrome' in webbrowser._browsers:
                        browser = webbrowser.get('google-chrome')
                    else:
                        # Register explicitly if found
                        import os
                        if os.path.exists(chrome_path):
                            webbrowser.register('chrome_manual', None, webbrowser.BackgroundBrowser(chrome_path))
                            browser = webbrowser.get('chrome_manual')
                        elif os.path.exists(chrome_path_x86):
                            webbrowser.register('chrome_manual', None, webbrowser.BackgroundBrowser(chrome_path_x86))
                            browser = webbrowser.get('chrome_manual')
                    
                    if browser:
                        browser.open(url)
                    else:
                        # Fallback to default
                        webbrowser.open(url)
                        
                except Exception as e:
                    print(f"Error launching specific browser, falling back to default: {e}")
                    webbrowser.open(url)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Launched! Server exiting...")
                
                # Shut down server
                threading.Thread(target=self.server.shutdown).start()
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing URL")

def run():
    ip = get_local_ip()
    url = f"http://{ip}:{PORT}"
    print(f"Server starting on {url}")
    print_qr(url)
    
    server = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    print("Server stopped.")

if __name__ == '__main__':
    run()
