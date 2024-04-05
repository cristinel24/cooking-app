from flask import Flask

app = Flask(__name__)


@app.get('/')
def get_root():
    return 'Request on root route!'


@app.get('/heartbeat')
def get_heartbeat():
    return 'Alive!'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
