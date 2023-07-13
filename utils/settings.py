import yaml
import os
import inspect

from os import getcwd
from os.path import abspath, join, exists

class Settings:
    def __init__(self):
        self.forbidden = ['path', 'settings', 'last_modified', 'load_settings', 'create_settings', 'update_settings', 'set_setting']

        self.path = abspath(join(getcwd(), 'settings.yaml'))

        self.last_modified = os.path.getmtime(self.path)
        self.settings = self.load_settings()
        self._updating = False

    def load_settings(self):
        settings = {}
        if exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                settings = yaml.safe_load(f) or {}
        else:
            self.create_settings()
        for key, value in settings.items():
            if key not in self.forbidden:
                self.__dict__[key] = value
        return settings

    def create_settings(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write("")

    def update_settings(self):
        self.settings = self.load_settings()

    def __getattribute__ (self, name):
        try:
            # Try the default behaviour first
            return super().__getattribute__(name)
        except AttributeError:
            # If an AttributeError was raised, return None
            return None

    def set_setting(self, key, value):
        if key in self.forbidden:
            raise ValueError(f'Key "{key}" is forbidden.')
        self.settings[key] = value
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(yaml.dump(self.settings))
        self.update_settings()

settings = Settings()


if __name__ == '__main__':
    #do some testing
    print(settings.settings)
    print(settings.path)
    print(settings.test)
    print(settings.eee)
    settings.set_setting('test', 'uu')
    print(settings.test)
    settings.set_setting('path', 'AAAAAAAAAAA')