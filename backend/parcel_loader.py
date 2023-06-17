import json
from io import open
from typing import Dict

from django.conf import settings


_loaders = {}


DEFAULT_CONFIG = {
    "DEFAULT": {
        "CACHE": not settings.DEBUG,
        "BUNDLE_DIR": "dist",
        "STATS_FILE": "static/dist/parcel-manifest.json",
    }
}


class ParcelLoader:
    _assets: Dict[str, str] = {}

    def __init__(self, name, config):
        self.name = name
        self.config = config

    def load_assets(self):
        try:
            with open(self.config["STATS_FILE"], encoding="utf-8") as f:
                return json.load(f)
        except IOError:
            raise IOError(
                "Error reading {0}. Are you sure parcel has generated "
                "the file and the path is correct?".format(self.config["STATS_FILE"])
            )

    def get_assets(self):
        if self.config["CACHE"]:
            if self.name not in self._assets:
                self._assets[self.name] = self.load_assets()
            return self._assets[self.name]
        return self.load_assets()

    def get_asset(self, asset_name):
        assets = self.get_assets()
        return self.config["BUNDLE_DIR"] + assets[asset_name]


def get_loader(config_name):
    if config_name not in _loaders:
        config = DEFAULT_CONFIG[config_name]
        _loaders[config_name] = ParcelLoader(config_name, config)
    return _loaders[config_name]
