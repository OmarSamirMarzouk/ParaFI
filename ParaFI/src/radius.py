from pyrad.server import Server
from pyrad.dictionary import Dictionary
from pyrad.packet import AccessAccept, AccessReject
import sqlite3
import select
import socket
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

class RadiusServer(Server):
    def __init__(self, dictionary_path, **kwargs):
        self.dictionary = Dictionary(dictionary_path)
        super().__init__(dict=self.dictionary, **kwargs)
        self.authsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.acctsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.authsock.bind(('', self.authport))
        self.acctsock.bind(('', self.acctport))
        logging.info(f"RADIUS Server initialized and bound to ports {self.authport} (auth) and {self.acctport} (acct)")
        self.ip_pool = iter([f"192.168.1.{i}" for i in range(100, 200)])  # Simple IP pool management

    def HandleAuthPacket(self, pkt):
        username = pkt["User-Name"][0]
        password = pkt["User-Password"][0]
        logging.info(f"Handling authentication request for user: {username}")

        if self.check_credentials(username, password):
            logging.info("Authentication successful")
            framed_ip = next(self.ip_pool, "192.168.1.255")  # Get next IP or use a default if pool is exhausted
            reply = self.CreateReplyPacket(pkt, **{
                "Service-Type": "Framed-User",
                "Framed-IP-Address": framed_ip
            })
            reply.code = AccessAccept
        else:
            logging.info("Authentication failed")
            reply = self.CreateReplyPacket(pkt)
            reply.code = AccessReject

        self.SendReplyPacket(pkt.fd, reply)

    def check_credentials(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        conn.close()
        return result is not None

    def Run(self):
        logging.info(f"RADIUS Server running on IP: {self.get_ip()} with secret: {self.hosts['localhost']['secret'].decode()}")

        try:
            while True:
                ready_sockets, _, _ = select.select([self.authsock, self.acctsock], [], [])
                for sock in ready_sockets:
                    data, addr = sock.recvfrom(4096)
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
            logging.error(f"Failed to decode authentication packet due to an exception: {e}")

    def HandleAcctSocket(self, data, addr):
        try:
            packet = self.CreatePacket(packet=data)
            self.HandleAcctPacket(packet)
        except Exception as e:
            logging.error(f"Failed to decode accounting packet due to an exception: {e}")

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
    dictionary_path = "dictionary.txt"
    srv = RadiusServer(dictionary_path=dictionary_path,
                       hosts={"localhost": {"secret": b"1111", "authport": 1812, "acctport": 1813}})
    srv.Run()
