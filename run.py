from flask_app import app
host1 = 'localhost'
host2 = '192.168.1.13'
if __name__ == '__main__':
    app.run(debug=True, host = host1, port=80)
