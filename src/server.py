from tornado import ioloop
from tornado import web
from tornpsql import Connection
import json
import logging
import os.path

import settings


class BaseHandler(web.RequestHandler):
    def initialize(self, db):
        self.db = db

class KillsByDay(BaseHandler):
    def get(self, _type, day):
        resp = self.db.query("""SELECT * FROM {table}_kills_daily where date=%s""".format(table=_type), (day))
        self.write(json.dumps(resp))

class KillsTotal(BaseHandler):
    def get(self, _type):
        resp = self.db.query("""SELECT * FROM {table}_kills_total""".format(table=_type))
        self.write(json.dumps(resp))

class VictoryPointsByDay(BaseHandler):
    def get(self, _type, day):
        raise web.HTTPError(405, "Method not implemented")

class VictoryPointsTotal(BaseHandler):
    def get(self, _type):
        raise web.HTTPError(405, "Method not implemented")

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    db = Connection('localhost', 'purgeboard', user=settings.PSQL_USER, password=settings.PSQL_PASSWORD)
    path = os.path.join(os.path.dirname(__file__), "static")
    routes = [
            (r"/static/(.*)", web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")}),
            (r"/(?P<_type>char|corp|faction)/kills/day/(?P<day>[0-9]{8})/?", KillsByDay, {"db": db}),
            (r"/(?P<_type>char|corp|faction)/kills/total/?", KillsTotal, {"db": db}),
            (r"/(?P<_type>char|corp|faction)/victory/day/(?P<day>[0-9]{8})/?", VictoryPointsByDay, {"db": db}),
            (r"/(?P<_type>char|corp|faction)/victory/total/?", VictoryPointsTotal, {"db": db}),
            ]
    application = web.Application(routes)
    application.listen(settings.LISTEN_PORT)
    logging.info("Server starting on port {port}".format(port=settings.LISTEN_PORT))
    ioloop.IOLoop.instance().start()
