from intake.container.base import RemoteSource, get_partition
from intake.source.base import DataSource, Schema


class RemoteAccLat(RemoteSource):
    """
    Accelerator lattice source on an intake server.
    """

    name = "remote_acclat"
    container = "acclat"

    def __init__(self, url, headers, **kwargs):
        super(RemoteAccLat, self).__init__(url, headers, **kwargs)
        self.npartitions = kwargs["npartitions"]
        self.shape = tuple(kwargs["shape"])
        self.metadata = kwargs["metadata"]
        self.dtype = kwargs["dtype"]
        self.verify = kwargs.get("verify", False)
        self._schema = Schema(
            npartitions=self.npartitions,
            extra_metadata={},
            dtype=self.dtype,
            shape=self.shape,
            datashape=None,
        )
        self._json = None
        self._madx = None
        self._lte = None
        self.twiss = None

    def _load_metadata(self):
        """
        Load the data from remote.

        Tricky thing here is that intake uses the code ´get_partition´ triggering
        the read or _get_partition from the local driver on the server side (see ../containers/AccLat.py).
        This returns a ´single object´, making it not so easy to return the data stored in the
        different files in a straightforwar way. Therefor I decided to the serverside plugin
        driver return a tuple of datasets, stored in attributes, 
        allowing for the different format return functions. The read or get_partition functions
        then return the easiest format - namely the latticejson format.
        """
        if self._json is None:
            self._json, self._madx, self._lte, self.twiss = get_partition(
                self.url, self.headers, self._source_id, self.container, None
            )

        return self._schema

    def _get_partition(self, _):
        # print("partition on remote")
        self._load_metadata()
        return self._json

    def read(self):
        # print("read on remote")
        self._load_metadata()
        return self._json

    def to_madx(self):
        # print("tomadx on remote")
        self._load_metadata()
        return self._madx

    def to_lte(self):
        self._load_metadata()
        return self._lte

    def to_twiss(self):
        self._load_metadata()
        return self.twiss

    @property
    def plot(self):
        """
        Returns a hvPlot object to provide a high-level plotting API.
        To display in a notebook, be sure to run ``intake.output_notebook()``
        first.

        Adapted from the original code to be able to plot the data
        stored in the twiss table files.
        """
        try:
            from hvplot import hvPlot
        except ImportError:
            raise ImportError(
                "The intake plotting API requires hvplot."
                "hvplot may be installed with:\n\n"
                "`conda install -c pyviz hvplot` or "
                "`pip install hvplot`."
            )
        metadata = self.metadata.get("plot", {})
        # print("hvplot meta", metadata)
        # fields = self.metadata.get("fields", {})
        # print("hv fields", fields)
        #     for attrs in fields.values():
        #         if 'range' in attrs:
        #             attrs['range'] = tuple(attrs['range'])
        #     metadata['fields'] = fields
        plots = self.metadata.get("plots", {})
        self._load_metadata()

        # print(hvPlot(self.twiss, custom_plots=plots, **metadata))
        return hvPlot(self.twiss, custom_plots=plots, **metadata)

    def _close(self):
        self._json = None
        self._madx = None
        self._lte = None
        self.twiss = None
