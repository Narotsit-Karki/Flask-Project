from flask_app import app
import socket
host = socket.gethostname()
host_ip = socket.gethostbyname(host)
host1 = 'localhost'

if __name__ == '__main__':
    app.run(debug=True, host = host, port=80)
