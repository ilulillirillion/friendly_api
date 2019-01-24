#!/usr/bin/env python3


from flask import jsonify
from .blueprint import app


@app.route('/hello_world')
def hello_world():
  return jsonify({'status':'hello'})
