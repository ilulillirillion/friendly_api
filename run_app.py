#!/usr/bin/env python3


import os
from core.app.blueprint import app


watch_directories = [ 'local', 'default' ]
watch_files = []
for watch_directory in watch_directories:
  for dirname, dirs, files in os.walk(watch_directory):
    for filename in files:
      filename = os.path.join(dirname, filename)
      print('test: {}'.format(filename))
      if not filename.endswith('.swp'):
        print('file does not end with swp')
        if os.path.isfile(filename):
          watch_files.append(filename)


if __name__ == '__main__':

  print('watch files: {}'.format(watch_files))
  app.run(host='0.0.0.0',debug=True, extra_files=watch_files)
