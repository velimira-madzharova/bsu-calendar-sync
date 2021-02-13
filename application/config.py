#!/usr/bin/env python3

import yaml

class Config:

    def __init__(self, config_file = 'config.yml'):
        with open(config_file, "r") as ymlfile:
             self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    def get(self, type):
        return self.cfg[type]