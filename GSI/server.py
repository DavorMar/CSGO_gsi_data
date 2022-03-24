from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import json

from GSI import payloadparser

"""
Server code mostly taken from https://github.com/Erlendeikeland/csgo-gsi-python, with a few tweaks.
"""

class GSIServer(HTTPServer):
    def __init__(self, server_address, auth_token):
        super(GSIServer, self).__init__(server_address, RequestHandler)

        self.auth_token = auth_token
        self.parser = payloadparser.PayloadParser()
        
        self.running = False

    def start_server(self):
        try:
            thread = Thread(target=self.serve_forever)
            thread.start()
            first_time = True
            while self.running == False:
                if first_time == True:
                    print("CS:GO GSI Server starting..")
                first_time = False
        except:
            print("Could not start server.")

    def get_data(self):
        return self.parser



class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")

        payload = json.loads(body)

        with open ("data_for_parse.json", "w") as file:
            json.dump(payload,file)


        if not self.authenticate_payload(payload):
            print("auth_token does not match.")
            return False
        else:
            self.server.running = True

        if len(payload) <5 or payload["phase_countdowns"]["phase"] == "warmup" or "round" not in payload:
            self.server.parser.empty_data()
        else:
            self.server.parser.parse_data(payload)


    def authenticate_payload(self, payload):
        if "auth" in payload and "token" in payload["auth"]:
            return payload["auth"]["token"] == self.server.auth_token
        else:
            return False
