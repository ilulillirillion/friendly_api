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
  def add_host_to_inventory(ip_address, hostname=None, inventory_path=app.configuration['ansible']['inventory_path']):
    if hostname is None:
      hostname = ip_address
    with open('/etc/hosts', 'r') as f:
      lines = f.readlines()
    with open('/etc/hosts', 'w') as f:
      for line in lines:
        if not line.startswith(ip_address):
          f.write(line)
      f.write('{}  {}'.format(ip_address, hostname))
    group_definitions = AnsibleApi.parse_group_definitions()
    #inventory_path = app.configuration['ansible']['inventory_path']
    for group_definition in group_definitions:
      print('considering group definition: <{}>'.format(group_definition['name']))
      hostfile = '{}/{}.ini'.format(inventory_path, group_definition['name'])
      if 'regex' in group_definition and re.compile(group_definition['regex']).match(hostname):
        AnsibleApi.add_host_to_hostfile(hostname, hostfile)
      elif 'add_exceptions' in group_definition:
        print('processing add exceptions')
        for exception in group_definition['add_exceptions']:
          print('processing exception: <{}>'.format(exception))
          if exception == hostname:
            print('exception (<{}>) matches <{}>'.format(exception, hostname))
            AnsibleApi.add_host_to_hostfile(hostname, hostfile)
  
  @staticmethod
  def add_host_to_hostfile(hostname, hostfile, avoid_duplicates=True):
    print('adding <{}> to <{}>'.format(hostname, hostfile))
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
        ip_address = request.json['ip_address']
      except NameError:
        return jsonify({'status':"missing required parameter: 'ip_address'!" })
      inventory_path = app.configuration['ansible']['inventory_path']
      if 'inventory_path' in request.json:
        inventory_path = request.json['inventory_path']
      hostname = None
      if 'hostname' in request.json:
        hostname = request.json['hostname']
      AnsibleApi.add_host_to_inventory(ip_address, hostname, inventory_path)

  class RunPlaybook(Resource):
    def post(self):
      print('executing playbook')
      hosts = 'all'
      playbook = app.configuration['ansible']['default_playbook']
      inventory = app.configuration['ansible']['inventory_path']
      if 'playbook' in request.json:
        playbook = request.json['playbook']
      if 'inventory_path' in request.json:
        inventory = request.json['inventory_path']
      if 'hosts' in request.json:
        hosts = request.json['hosts']
      os.system("ansible-playbook {} -i {} -l {},".format(playbook, inventory, hosts))


app.api.add_resource(AnsibleApi.AddHost, '/api/ansible', '/api/ansible/add_host', endpoint='/api/ansible/add_host')
app.api.add_resource(AnsibleApi.RunPlaybook, '/api/ansible/run_playbook', endpoint='/api/ansible/run_playbook')
