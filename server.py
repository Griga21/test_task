import uuid, logging

from datetime import datetime
from urllib.parse import parse_qs
from twisted.internet import reactor
from twisted.web import resource, server

from db import Database
from config import (
    SERVER_UUID,
    CLIENT_UUID,
    MESSAGE,
    SUCCESS_TEXT,
    SERVER_UUID_HEADER,
    CLIENT_UUID_HEADER,
    config
)


class MyResource(resource.Resource):
    isLeaf = True
    params = {}

    def render_POST(self, request):
        self.params = self.__get_params_in_dict(request)

        active_port = request.__dict__['host'].__dict__['port']

        registration_condition = CLIENT_UUID in self.params and SERVER_UUID not in self.params
        authentication_condition = CLIENT_UUID in self.params and SERVER_UUID in self.params

        if registration_condition and active_port == config['path']['registration_port']:
            return self.__registration(request)


        elif authentication_condition and active_port == config['path']['authentication_port']:
            return self.__authentication(request)

        else:
            return '{0}'.format(config['text']['error']).encode('utf-8')


    def __registration(self, request):
        server_uuid = str(uuid.uuid4())

        db.insert_registration(self.params[CLIENT_UUID], server_uuid, datetime.now())

        request.setHeader(SERVER_UUID_HEADER, server_uuid)
        return ''.encode('utf-8')


    def __authentication(self, request):
        res = db.select_one_registration(self.params[CLIENT_UUID], self.params[SERVER_UUID])

        if not res:
            request.setHeader('Status', 'Authentication error')
            return '{0}'.format(config['text']['error']).encode('utf-8')

        request.setHeader('Status', 'Authentication success')
        request.setHeader(SERVER_UUID_HEADER, self.params[SERVER_UUID])
        request.setHeader(CLIENT_UUID_HEADER, self.params[CLIENT_UUID])

        # check message from client
        try:
            message = self.params[MESSAGE]
        except:
            message = False

        if message:
            row = tuple(res)
            logging.info('{0}: [{1}] ({2}) {3} {4}'.format(
                    datetime.now(),
                    SUCCESS_TEXT,
                    message,
                    row[0],
                    row[1]
                ))
            print('{0}: [{1}] ({2}) {3} {4}'.format(
                    datetime.now(),
                    SUCCESS_TEXT,
                    message,
                    row[0],
                    row[1]
                ))
        return ''.encode('utf-8')


    def __get_params_in_dict(self, request):
        params = parse_qs(request.content.read())
        dict_params = {}

        for key, value in params.items():
            dict_params[key.decode("utf-8")] = value[0].decode("utf-8")
        return dict_params


if __name__ == "__main__":
    db = Database()
    # db.drop_table()
    db.create_table()

    logging.basicConfig(filename=config['logging']['logfile_name'],
                        level=logging.INFO)
    site = server.Site(MyResource())

    reactor.listenTCP(config['path']['registration_port'], site)
    reactor.listenTCP(config['path']['authentication_port'], site)

    print(config['text']['server_started'].format(
            config['path']['protocol'],
            config['path']['host_name'],
            config['path']['registration_port'])
        )
    print(config['text']['server_started'].format(
            config['path']['protocol'],
            config['path']['host_name'],
            config['path']['authentication_port'])
        )

    reactor.run()
