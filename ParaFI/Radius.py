from pyrad.server import Server
from pyrad.dictionary import Dictionary
from pyrad.packet import AccessAccept, AccessReject
import sqlite3
import select
import socket
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RadiusServer(Server):
    def __init__(self, dictionary_path, **kwargs):
        self.dictionary = Dictionary(dictionary_path)
        super().__init__(dict=self.dictionary, **kwargs)
        self.authsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.acctsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.authsock.bind(('', self.authport))
        self.acctsock.bind(('', self.acctport))
        logging.info("RADIUS Server initialized and bound to authentication port {} and accounting port {}".format(self.authport, self.acctport))

    def HandleAuthPacket(self, pkt):
        username = pkt.get("User-Name", [None])[0]
        if username:
            logging.info("Handling authentication request for user: {}".format(username))
            self.send_response(pkt, AccessAccept, '192.168.1.100')  # Assuming IP assignment is static for simplification
        else:
            logging.error("Authentication request without username received")
            self.send_response(pkt, AccessReject)

    def send_response(self, pkt, code, ip_address=None):
        reply = self.CreateReplyPacket(pkt)
        reply.code = code
        if code == AccessAccept:
            reply["Framed-IP-Address"] = ip_address
        self.SendReplyPacket(pkt.fd, reply)

    def Run(self):
        try:
            while True:
                ready_sockets, _, _ = select.select([self.authsock, self.acctsock], [], [])
                for sock in ready_sockets:
                    data, addr = sock.recvfrom(4096)
                    logging.info("Packet received from {}: {}".format(addr, data))
                    if sock == self.authsock:
                        self.HandleAuthSocket(data, addr)
                    elif sock == self.acctsock:
                        self.HandleAcctSocket(data, addr)
        finally:
            self.authsock.close()
            self.acctsock.close()

    def HandleAuthSocket(self, data, addr):
        try:
            packet = self.CreatePacket(packet=data)
            self.HandleAuthPacket(packet)
        except Exception as e:
            logging.error("Failed to process authentication packet due to an exception")
            logging.error(traceback.format_exc())

    def HandleAcctSocket(self, data, addr):
        try:
            packet = self.CreatePacket(packet=data)
            self.HandleAcctPacket(packet)
        except Exception as e:
            logging.error("Failed to process accounting packet due to an exception")
            logging.error(traceback.format_exc())

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

if __name__ == "__main__":
    dictionary_path = "C:\\Users\\Omar\\Desktop\\ParaFI\\data\\dictionary.txt"
    srv = RadiusServer(dictionary_path=dictionary_path,
                       hosts={"localhost": {"secret": b"1111", "authport": 1812, "acctport": 1813}})
    srv.Run()
