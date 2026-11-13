#!/usr/bin/env python3
"""Serves index.html and forwards browser calls to CXone, avoiding CORS.

Run:  python3 server.py   then open http://localhost:8080
The page sends requests to /proxy with the real destination in X-Target-URL.
Only https targets are forwarded. Listens on localhost only.
"""
import http.server, urllib.request, urllib.error, os
from urllib.parse import urlparse

PORT = 8080
ROOT = os.path.dirname(os.path.abspath(__file__))
DROP = {'host', 'origin', 'referer', 'x-target-url', 'connection', 'content-length',
        'accept-encoding', 'sec-fetch-mode', 'sec-fetch-site', 'sec-fetch-dest'}


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def _proxy(self):
        target = self.headers.get('X-Target-URL', '')
        if urlparse(target).scheme != 'https':
            self.send_error(400, 'X-Target-URL must be an https URL')
            return
        n = int(self.headers.get('Content-Length') or 0)
        body = self.rfile.read(n) if n else None
        hdrs = {k: v for k, v in self.headers.items() if k.lower() not in DROP}
        req = urllib.request.Request(target, data=body, method=self.command, headers=hdrs)
        try:
            r = urllib.request.urlopen(req, timeout=300)
            status, data, ctype = r.status, r.read(), r.headers.get('Content-Type', 'application/json')
        except urllib.error.HTTPError as e:
            status, data, ctype = e.code, e.read(), e.headers.get('Content-Type', 'application/json')
        except Exception as e:
            status, data, ctype = 502, str(e).encode(), 'text/plain'
        self.send_response(status)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        self._proxy() if self.path == '/proxy' else self.send_error(404)

    do_PUT = do_POST

    def do_GET(self):
        self._proxy() if self.path == '/proxy' else super().do_GET()


if __name__ == '__main__':
    print(f'Open http://localhost:{PORT}')
    http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
