from intake.source import base
from intake.container.base import RemoteSource
import fsspec
import json
import pandas as pd 

class LocalAccLat(RemoteSource):
    name = 'local-acclat'
    container = 'python'

    def __init__(self, filebase, metadata=None):
        self._schema = None
        self.filebase = filebase
        self.metadata = metadata
        self._json = None
        self._madx = None

        print(filebase)
    def _load(self, _type):
        fs = fsspec.filesystem('file')
        if _type == 'json':
            with fs.open(self.filebase + ".json") as f:
                self._json = json.loads(f.read())
        elif _type == 'madx':
            with fs.open(self.filebase + ".madx") as f:
                self._madx = f.read()
        else:
            raise ValueError('Invalid lattice format.')

    def _get_schema(self):
        return base.Schema(
            datashape = None,
            dtype = None,
            shape = None,
            npartitions = None,
            extra_metadata = {}
        )

    def _get_partition(self, _):
        if self._json is None:
            self._load(_type='json')
        if self._madx is None:
            self._load(_type='madx')
        return self._json


    def read(self, _type):
        if self._json is None:
            self._load(_type='json')
            return self._json
        if self._madx is None:
            self._load(_type='madx')
            return self._madx
        return self._json

    def _close(self):
        self._json = None
        self._madx = None