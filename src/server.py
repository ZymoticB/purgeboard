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

class IndexHandler(BaseHandler):
    def get(self):
        self.redirect('/static/app/index.html', permanent=True)

class KillsByDay(BaseHandler):
    def get(self, _type, day):
        resp = self.db.query("""SELECT * FROM {table}_kills_daily where date=%s""".format(table=_type), (day))
        self.write(json.dumps(resp, indent=4, sort_keys=True))

class KillsTotal(BaseHandler):
    def get(self, _type):
        resp = self.db.query("""SELECT * FROM {table}_kills_total""".format(table=_type))
        self.write(json.dumps(resp, indent=4, sort_keys=True))

class VictoryPointsByDay(BaseHandler):
    def get(self, _type, day):
        raise web.HTTPError(405, "Method not implemented")

class VictoryPointsTotal(BaseHandler):
    def get(self, _type):
        raise web.HTTPError(405, "Method not implemented")

class CorpStats(BaseHandler):
    def get(self, corp, date=None):
        if date:
            resp = self.db.get("""SELECT * FROM {corp}_fw_stats where date=%s""".format(corp=corp), (date))
        else:
            resp = self.db.get("""SELECT * FROM {corp}_fw_stats where date = (SELECT max(date) FROM {corp}_fw_stats)""".format(corp=corp), ())
        self.write(json.dumps(resp, indent=4, sort_keys=True))


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    db = Connection('localhost', 'purgeboard', user=settings.PSQL_USER, password=settings.PSQL_PASSWORD)
    path = os.path.join(os.path.dirname(__file__), "static")
    routes = [
            (r"/", IndexHandler, {"db": db}),
            (r"/(favicon.ico)", web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")}),
            (r"/static/(.*)", web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")}),
            (r"/(?P<_type>char|corp|faction)/kills/day/(?P<day>[0-9]{8})/?", KillsByDay, {"db": db}),
            (r"/(?P<_type>char|corp|faction)/kills/total/?", KillsTotal, {"db": db}),
            (r"/(?P<_type>char|corp|faction)/victory/day/(?P<day>[0-9]{8})/?", VictoryPointsByDay, {"db": db}),
            (r"/(?P<_type>char|corp|faction)/victory/total/?", VictoryPointsTotal, {"db": db}),
            (r"/(?P<corp>[A-Za-z0-9 .-]+)/?", CorpStats, {"db": db}),
            (r"/(?P<corp>[A-Za-z0-9 .-]+)/(?P<date>[0-9]{8})/?", CorpStats, {"db": db}),
            ]
    application = web.Application(routes)
    application.listen(settings.LISTEN_PORT)
    logging.info("Server starting on port {port}".format(port=settings.LISTEN_PORT))
    ioloop.IOLoop.instance().start()
