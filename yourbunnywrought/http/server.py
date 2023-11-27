import contextlib
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import socket

__all__ = ['init_cli', 'invoke_cli', 'serve_static']


class ServerClass(ThreadingHTTPServer):
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


def serve_static(directory, host='', port=4848):
    ServerClass.address_family, server_address = _get_best_family(host, port)
    HandlerClass = partial(SimpleHTTPRequestHandler, directory=directory)
    with ServerClass(server_address, HandlerClass) as server:
        host, port = server.socket.getsockname()[:2]
        url_host = f'[{host}]' if ':' in host else host
        print(f'Listening on http://{url_host}:{port}/')
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


def init_cli(parent, ArgTypes):
    parser = parent.add_parser('serve_static', add_help=False)

    parser.add_argument(
        'directory',
        type=ArgTypes.existing_path_type,
        default=Path.cwd(),
        nargs='?',
    )

    return ['serve_static']


def invoke_cli(args):
    match args.command:
        case 'serve_static':
            serve_static(args.directory)
