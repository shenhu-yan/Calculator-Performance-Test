#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os

PORT = 3000

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"\n{'='*60}")
    print(f"  🚀 HTTP服务器已启动")
    print(f"  📂 访问地址: http://localhost:{PORT}/calculator.html")
    print(f"  {'='*60}\n")
    print("按 Ctrl+C 停止服务器\n")
    
    webbrowser.open(f'http://localhost:{PORT}/calculator.html')
    
    httpd.serve_forever()