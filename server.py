#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys

# Set the directory before any imports that use getcwd
website_dir = '/Users/artembagryantsev/Documents/Claude Code/Window Cleaning website/website'
os.chdir(website_dir)

port = int(os.environ.get('PORT', 8000))

class Handler(http.server.SimpleHTTPRequestHandler):
    pass

with socketserver.TCPServer(("", port), Handler) as httpd:
    print(f"Server running on http://localhost:{port}")
    httpd.serve_forever()
