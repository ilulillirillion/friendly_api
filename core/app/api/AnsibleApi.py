#!/usr/bin/env python3


import os
import re
from flask import jsonify, request
from flask_restful import Resource
from ..blueprint import app


class AnsibleApi():

  @staticmethod
  def parse_group_definitions():
    group_definitions = app.configuration['ansible']['group_definitions']
    group_definitions_files = app.configuration['ansible']['group_definitions_files']
    for group_definitions_file in group_definitions_files:
      group_definitions_data = app.data_parser.read_yaml(group_definitions_file)
      group_definitions = group_definitions + group_definitions_data
    return group_definitions

  @staticmethod
  def add_host_to_inventory(network_address, hostname=None):
    if hostname is None:
      hostname = network_address
    group_definitions = AnsibleApi.parse_group_definitions()
    inventory_path = app.configuration['ansible']['inventory_path']
    for group_definition in group_definitions:
      if re.compile(group_definition['regex']).match(hostname):
        hostfile = '{}/{}.ini'.format(inventory_path, group_definition['name'])
        AnsibleApi.add_host_to_hostfile(hostname, hostfile)
  
  @staticmethod
  def add_host_to_hostfile(hostname, hostfile, avoid_duplicates=True):
    found_duplicate_host = False
    if not os.path.exists(hostfile):
      with open(hostfile, 'a+') as f:
        group_name = os.path.splitext(os.path.basename(hostfile))[0]
        f.write('[{}]\n'.format(group_name))
    else:
      with open(hostfile, 'r') as f:
        lines = f.readlines()
      for line in lines:
        if line.rstrip() == hostname:
          found_duplicate_host = True
    if not found_duplicate_host and avoid_duplicates:
      with open(hostfile, 'a+') as f:
        f.write('{}\n'.format(hostname))

  class AddHost(Resource):
    @app.security_handler.authorization_required
    def post(self):
      print('handling add_host request: <{}>'.format(request))
      try:
        network_address = request.json['network_address']
      except NameError:
        return jsonify({'status':"missing required parameter: 'network_address'!" })
      hostname = None
      if 'hostname' in request.json:
        hostname = request.json['hostname']
      AnsibleApi.add_host_to_inventory(network_address, hostname)


app.api.add_resource(AnsibleApi.AddHost, '/api/ansible', '/api/ansible/add_host', endpoint='/api/ansible/add_host')
