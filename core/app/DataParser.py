#!/usr/bin/env python3


import os
import yaml


class DataParser():
  
  @staticmethod
  def read_yaml(filepath):
    if not os.path.exists(filepath):
      print('<{}> not found!'.format(filepath))
      yaml_contents = {}
    else:
      with open(filepath, 'r') as f:
        yaml_contents = yaml.safe_load(f)
      return yaml_contents
