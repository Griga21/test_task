# constants
SERVER_UUID = 'server_uuid'
CLIENT_UUID = 'client_uuid'
MESSAGE = 'message'
SUCCESS_TEXT = 'success'
SERVER_UUID_HEADER = 'Server-Uuid'
CLIENT_UUID_HEADER = 'Client-Uuid'

config = {
    'path': {
        'protocol': 'http://',
        'host_name': 'localhost',
        'registration_port': 8000,
        'authentication_port': 8001
    },
    'text': {
        'error': 'Error',
        'server_started': 'Server started: {0}{1}:{2}',
    },
    'logging': {
        'logfile_name': 'logfile.log',
    },
    'database': {
        'database_name': 'database.db'
    }
}