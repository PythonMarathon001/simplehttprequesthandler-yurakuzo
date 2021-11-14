import json
from http.server import HTTPServer, BaseHTTPRequestHandler

USERS_LIST = [
    {
        "id": 1,
        "username": "theUser",
        "firstName": "John",
        "lastName": "James",
        "email": "john@email.com",
        "password": "12345",
    }
]


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_response(self, status_code=200, body=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body if body else {}).encode('utf-8'))

    def _pars_body(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        return json.loads(self.rfile.read(content_length).decode('utf-8'))  # <--- Gets the data itself
    
    def do_GET(self):
            status = 200

            if self.path == "/users":
                body = USERS_LIST
                return self._set_response(status, body)

            for data in USERS_LIST:
                if self.path == f"/user/{data['username']}":
                    body = data
                    return self._set_response(status, body)
                else:
                    status = 400
                    body = {'error': 'User not found'}
            
                    return self._set_response(status, body)
    def do_POST(self):
        data = self._pars_body()
        
        if isinstance(data, dict):
            data = [data]

        try:
            id_list = [data['id'] for data in USERS_LIST]
        
            for data in data:
                if data["id"] not in id_list:
                    id_list.append(data["id"])
                else:
                    return self._set_response(400)

        except KeyError:
            return self._set_response(400)
        
        status = 201
        body = data
        
        if len(body) == 1:
            return self._set_response(status, body[0])   
        
        return self._set_response(status, body)   

    def do_PUT(self):
        pars = self._pars_body()

        check_valid_data = ["username", "firstName", "lastName", "email", "password"]

        for data in USERS_LIST:
            if check_valid_data == list(pars.keys())\
            and self.path == f"/user/{data['username']}":
                pars.update({'id': data['id']})
                status = 200
                body = pars
                return self._set_response(status, body)
            
            elif self.path != f"/user/{data['username']}":
                status = 404
                body = {'error': 'User not found'}
                return self._set_response(status, body)

            else:
                status = 400
                body = {"error": "not valid request data"}
                return self._set_response(status, body)

    def do_DELETE(self):
        for data in USERS_LIST:
            if self.path == f"/user/{data['id']}":
                status = 200
                body = {}
                return self._set_response(status, body)
            else:
                status = 404
                body = {'error': 'User not found'}
                return self._set_response(status, body)


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, host='localhost', port=8000):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
