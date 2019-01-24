#!/usr/bin/env python3


from flask import jsonify
from flask_restful import Resource
from ..blueprint import app


class Info(Resource):
  
  @app.security_handler.authorization_required
  def get(self, drilldown=None):
    info = app.configuration
    print('drilldown: <{}>'.format(drilldown))
    if drilldown:
      drilldowns = drilldown.split('/')
      for drilldown in drilldowns:
        info = info[drilldown]
    return jsonify(info)


app.api.add_resource(Info, '/api/info', '/api/info/<path:drilldown>', endpoint='/api/info')
