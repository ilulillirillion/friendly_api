#!/usr/bin/env python3


import yaml
import os


#configuration = {}
#inline_configuration['configuration_test_variable_1'] = 1
configuration_filepaths = [
  'default/config.yaml',
  'local/config.yaml'
]


def read_yaml(filepath):
  if not os.path.exists(filepath):
    print('attempted to read non-existent file <{}>!'.format(filepath))
  else:
    with open(filepath, 'r') as f:
      yaml_contents = yaml.safe_load(f)
    return yaml_contents


def merge_recursively(*args):

  merged_data = {}

  for data_source in args:
    print('Processing data_source: <{}>'.format(data_source))
    if not isinstance(data_source, dict):
      print("expected <{}> to be a dictionary but it's not!".format(data_source))
      data_source = {}

    for key, value in data_source.items():
      print('Considering <{}> for recursive merge'.format(key))
      if (key in merged_data and
          (isinstance(value, dict) or
          isinstance(merged_data[key], dict))):
        print('Recursively merging <{}>'.format(key))
        #merged_data[key] = recursive_merge(merged_data[key], data_source[key])
        merged_data[key] = merge_recursively(merged_data[key], data_source[key])
      else:
        print('Overwriting key <{}>'.format(key))
        merged_data[key] = data_source[key]

  return merged_data


def merge_configuration_data(data_sources):
  inline_configuration = {'inline_test_variable': 1}
  configuration_data = []
  configuration_data.append(inline_configuration)
  for data_source in data_sources:
    print('parsing configuration source <{}>'.format(data_source))
    #configuration_data = read_yaml(data_source)
    data = read_yaml(data_source)
    configuration_data.append(data)
  configuration = merge_recursively(configuration_data)
  return configuration


def parse_configuration(configuration_sources):
  #configuration = merge_configuration_data(configuration_sources)

  configuration = {}
  for configuration_source in configuration_sources:

    # Check if it's a filepath
    if True:
      configuration_data = read_yaml(configuration_source)
      configuration = merge_recursively(configuration, configuration_data)

    else:
      #print(f'only supports filepaths for now')
      return None

  return configuration


configuration = parse_configuration(configuration_filepaths)
#print(f'Final configuration: <{configuration}>')
print('Final configuration: <{}>'.format(configuration))
