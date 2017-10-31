from bcrypt import hashpw
from eve.auth import BasicAuth
from flask import request, current_app as app


class BCryptAuthUser(BasicAuth):
    def check_auth(self, email, password, allowed_roles, resource, method):
        users = app.data.driver.db['user']
        auth_user = users.find_one({'email': email})
        return auth_user and hashpw(password, str(auth_user['password'])) == str(auth_user['password'])
