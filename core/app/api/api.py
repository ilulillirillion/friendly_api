#!/usr/bin/env python3


from flask_restful import Api
from ..blueprint import app


app.api = Api(app)
