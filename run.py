# -*- coding: utf-8 -*-
from app import create_app, io

app = create_app()

if __name__ == '__main__':
    # Local test
    # app.settings['X_DOMAINS'] = '*'
    io.run(app, host='0.0.0.0', port=5000, debug=True)
