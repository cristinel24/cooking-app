from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
DEBUG_MODE = bool(os.getenv('DEBUG_MODE', 'False'))

app = Flask(__name__)


@app.get('/')
def get_root():
    return 'Request on root route!'


@app.get('/heartbeat')
def get_heartbeat():
    return 'Alive!'


if __name__ == '__main__':
    app.run(port=FLASK_PORT, debug=DEBUG_MODE)
