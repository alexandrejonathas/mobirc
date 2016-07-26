import os

address = dict({
    'host': '0.0.0.0',
    'port': 38268
})

MESSAGE_BUFFER = 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates/')
