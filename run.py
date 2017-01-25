# -*- coding: utf-8 -*-

from eve import Eve
from settings import SETTINGS

app = Eve(settings=SETTINGS)

if __name__ == '__main__':
    # Local test
    app.run(host='127.0.0.1', port=5000, debug=True)
