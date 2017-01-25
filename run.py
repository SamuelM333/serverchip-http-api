# -*- coding: utf-8 -*-

from eve import Eve
from settings import SETTINGS

# Add environment variable detection here
# host = '127.0.0.1'
host = '0.0.0.0'
port = 5000

app = Eve(settings=SETTINGS)

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
