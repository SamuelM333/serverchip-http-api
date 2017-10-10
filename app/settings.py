# -*- coding: utf-8 -*-
from auth import BCryptAuthUser, BCryptAuthSnippet

GPIO_PORTS = [0, 2, 3, 4, 5, 10, 12, 13, 14, 15]
HOUR_REGEX = '^(([0-1]?[0-9])|([2][0-3])):([0-5]?[0-9])$'  # 24h regex
EMAIL_REGEX = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

user = {
    'item_title': 'user',
    'cache_control': '',
    'cache_expires': 0,
    'resource_methods': ['GET', 'POST'],
    'public_methods': ['POST'],
    'item_methods': ['GET', 'PATCH', 'PUT'],
    'public_item_methods': ['GET'],
    # 'authentication': BCryptAuthUser,
    'schema': {
        'name': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 120,
            'required': True,
        },
        'last_name': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 120,
        },
        'email': {
            'type': 'string',
            'minlength': 8,
            'maxlength': 255,
            'required': True,
            'unique': True,
            'regex': EMAIL_REGEX
        },
        'password': {
            'type': 'string',
            'minlength': 8,
            'maxlength': 255,
            'required': True
        },
        'role': {
            'type': 'string',
            'allowed': ['user', 'admin', 'superuser'],
            'default': 'user',
            'required': True
        }
    },
    'additional_lookup': {
        'url': 'regex("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")', # TODO Use EMAIL_REGEX here
        'field': 'email'
    }
}

microchip = {
    'item_title': 'microchip',
    'cache_control': '',
    'cache_expires': 0,
    'resource_methods': ['GET', 'POST'],
    'public_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'PUT', 'DELETE'],
    'public_item_methods': ['GET'],
    # 'authentication': BCryptAuthSnippet,
    'schema': {
        'name': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 60,
            'required': True
        },
        'owner': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'user',
                # make the owner embeddable with ?embedded={"owner":1}
                'embeddable': True
            }
        },
        'description': {
            'type': 'string',
            'minlength': 3,
            'maxlength': 120,
        },
        'ip': {
            'type': 'string',
            'minlength': 3,
            'maxlength': 120,
            'required': True,
            'unique': True,
            'regex': "(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$|^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*"
        }
    }
}

task = {
    'item_title': 'tasks',
    'cache_control': '',
    'cache_expires': 0,
    'resource_methods': ['GET', 'POST'],
    'public_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'PUT', 'DELETE'],
    'public_item_methods': ['GET'],
    # 'authentication': BCryptAuthSnippet,
    'schema': {
        'name': {'type': 'string', 'required': True, 'maxlength': 60},
        'description': {'type': 'string', 'maxlength': 120},
        'microchip': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'microchip',
                # embeddable with ?embedded={"microchip":1}
                'embeddable': True
            }
        },
        'output_port': {
            'type': 'dict',
            'required': True,
            'schema': {
                'number': {
                    'type': 'integer',
                    'required': True,
                    'allowed': GPIO_PORTS
                },
                'state': {'type': 'boolean', 'required': True}
            }
        },
        'conditions': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'name': {'type': 'string', 'required': True, 'maxlength': 60},
                    'day_hour': {
                        'type': 'dict',
                        'schema': {
                            'days': {
                                'type': 'string',
                                'required': True,
                                'allowed': [
                                    'Monday', 'Tuesday', 'Wednesday',
                                    'Thursday', 'Friday', 'Saturday', 'Sunday'
                                ]
                            },
                            'hour': {
                                'type': 'dict',
                                'required': True,
                                'schema': {
                                    'start': {'type': 'string', 'required': True, 'regex': HOUR_REGEX},
                                    'end': {'type': 'string', 'required': True, 'regex': HOUR_REGEX}
                                }
                            }
                        }
                    },
                    'input_port': {  # TODO Change to support numeric and boolean values
                        'type': 'dict',
                        'schema': {
                            'number': {
                                'type': 'integer',
                                'required': True,
                                'allowed': GPIO_PORTS
                            },
                            'state': {'type': 'boolean', 'required': True}
                        }
                    }
                }
            }
        }
    }
}

report = {
    'item_title': 'report',
    'cache_control': '',
    'cache_expires': 0,
    'resource_methods': ['GET', 'POST'],
    'public_methods': ['GET', 'POST'],
    'item_methods': ['GET'],
    'public_item_methods': ['GET'],
    # 'authentication': BCryptAuthSnippet,
    'schema': {
        'microchip': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'microchip',
                # embeddable with ?embedded={"microchip":1}
                'embeddable': True
            },
        },
        'details': {
            'type': 'dict',
            'schema': {
                'task_name': {'type': 'string', 'required': True},
                'status': {
                    'type': 'dict',
                    'schema': {
                        'code': {'type': 'string', 'allowed': ['Executed', 'Not Executed', 'Aborted']},
                        'reason': {
                            'type': 'string',
                            'allowed': [
                                'Conditions were given',
                                'Conditions were not given',
                                'User override'
                            ]
                        },
                        'user': {
                            'type': 'objectid',
                            'required': True,
                            'data_relation': {
                                'resource': 'user',
                                # embeddable with ?embedded={"user":1}
                                'embeddable': True
                            },
                        },
                    }
                }
            }
        }
    }
}

SETTINGS = {
    'DOMAIN': {
        'user': user,
        'microchip': microchip,
        'task': task,
        'report': report,
    },
    'MONGO_DBNAME': 'serverchip',
    'DATE_CREATED': 'created',
    # 'MONGO_USERNAME': '<your username>',
    # 'MONGO_PASSWORD': '<your password>',
    # 'MONGO_AUTH_SOURCE': None,
    # 'MONGO_AUTH_MECHANISM': None,
    'X_DOMAINS': ['*'],
    'X_HEADERS': ['If-Match', 'Authorization', 'Content-type'],
    'XML': False,
    'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
    'ITEM_METHODS': ['GET', 'PATCH', 'DELETE'],
    # 'AUTH_FIELD': "ID_FIELD"
}
