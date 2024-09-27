#!/usr/bin/python3

# 2024-01-03: copied from ~/git/website-check/

import sys
import socket
import socketserver
import _thread
import threading
from http.server import SimpleHTTPRequestHandler

# TODO make it quiet
# https://stackoverflow.com/questions/56227896/how-do-i-avoid-the-console-logging-of-http-server


class TCPServerReuseAddress(socketserver.TCPServer):
    allow_reuse_address = True
    address_family = socket.AF_INET6
    # TODO make the socket dualstack
    # -> it's not so easiy, because its a attribute for the socket!


class DefaultRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(404)  # Not Found
        self.end_headers()



# See also https://github.com/python/cpython/blob/main/Lib/test/test_httpservers.py#L47
class LocalWebserver:
    def __init__(self, port, request_handler=None):
        self._port = port
        if request_handler is None:
            self._request_handler = DefaultRequestHandler
        else:
            self._request_handler = request_handler

    def __enter__(self):
        self._httpd = TCPServerReuseAddress(("::1", self._port), self._request_handler)

        def f():
            # The following call uses polling internall to check for the exit
            # flag, that is set by 'shutdown()'
            self._httpd.serve_forever()
            self._httpd.server_close()

        self._t = threading.Thread(target=f)
        self._t.start()

        return None

    def __exit__(self, *args):
        self._httpd.shutdown()
        self._t.join()


if __name__ == "__main__":
    # Test
    pass # TODO
