#!/usr/bin/env python3


### Build application - base
from .app import app
from .hello_world import app

### Build application - api
from .api.api import app
from .api.Info import app
from .api.AnsibleApi import app
