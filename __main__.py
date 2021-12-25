import logging
import socket
import socketserver


IP = 'localhost'
PORT = 10001


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class BroadcastHandler(socketserver.BaseRequestHandler):
    @staticmethod
    def broadcast(data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(data, ('255.255.255.255', 0))
        sock.close()

    def handle(self):
        data = self.request[0]
        log.info('received: {}\n\tbroadcasting...'.format(data))
        self.broadcast(data)


def main():
    log.info('starting bigmouth server...')
    with socketserver.UDPServer((IP, PORT), BroadcastHandler) as server:
        server.serve_forever()


if __name__ == '__main__':
    main()
