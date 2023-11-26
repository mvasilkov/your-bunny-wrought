import contextlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import socket


class DualStackServer(ThreadingHTTPServer):
    def server_bind(self):
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()


def _get_best_family(*address):
    addrlist = socket.getaddrinfo(
        *address,
        type=socket.SOCK_STREAM,
        flags=socket.AI_PASSIVE,
    )
    # family, type, proto, canonname, sockaddr
    return addrlist[0][0], addrlist[0][4]


def serve_static():
    pass
