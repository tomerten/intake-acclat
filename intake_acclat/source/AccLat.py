import fsspec
import pandas as pd
from intake.source import base
from pandas.testing import assert_frame_equal


class AccLatSource(base.DataSource):
    """
    An accelerator lattice source.

    Parameters:
    -----------
    urlpath: str 
        path to lattice files excluding the extension 
        file extensions are reserved for the specific formats.
    """

    name = "acclatsource"
    container = "acclat"
    version = "0.0.1"

    def __init__(self, urlpath, metadata=None):
        self.urlpath = urlpath
        self._json = None
        self._madx = None
        self._lte = None
        self.twiss = None

        super(AccLatSource, self).__init__(metadata=metadata)

    def _get_schema(self):
        import fsspec
        import json

        urlpath = self._get_cache(self.urlpath)[0]
        fs = fsspec.filesystem("file")

        # read json file
        if self._json is None:
            with fs.open(urlpath + ".json") as f:
                self._json = json.loads(f.read())

        # read madx file
        if self._madx is None:
            # print(urlpath + ".madx")
            # import os
            # print(os.path.isfile(urlpath + ".madx"))

            with fs.open(urlpath + ".madx") as f:
                self._madx = f.read().decode("ascii")

        # read elegant file
        if self._lte is None:
            with fs.open(urlpath + ".lte") as f:
                self._lte = f.read().decode("ascii")

        # read twiss table and header
        # add header data to metadata
        if self.twiss is None:
            self.twiss = get_twissdata(urlpath + ".twiss")

            meta = pd.read_csv(
                urlpath + ".params", delim_whitespace=True, skiprows=4, error_bad_lines=False
            )
            # meta = get_tfsheader(urlpath + ".twiss").set_index("NAME")["VALUE"].to_dict()

        return base.Schema(
            datashape=None,
            dtype=None,
            shape=(None,),
            npartitions=self.npartitions,
            extra_metadata=meta,
        )

    def _get_partition(self, i):
        print("partition on local")
        return self._json

    def read(self):
        # print("read on local")
        return self._json, self._madx, self._lte, self.twiss

    def to_madx(self):
        # print("tomadx on local")
        return self._madx

    def to_lte(self):
        # print("lte on local")
        return self._lte

    def to_twiss(self):
        # print("twiss on local")
        return self.twiss

    def _close(self):
        self._json = None


def get_twisscolumns(tfsfile):
    """
    Reads the headers of the columns of the twiss file
    :param tfsfile:  file where twiss output is stored
    :return: list of strings
    """
    cols = pd.read_csv(tfsfile, delim_whitespace=True, skiprows=range(46), nrows=2, index_col=None)
    return list(cols.columns[1:].values)


def get_tfsheader(tfsfile):
    """
    Read the header part of the twiss data (e.g. particle energy, mass, etc...)
    :param tfsfile: file where twiss output is stored
    :return: dataframe containing the header data
    """
    headerdata = pd.read_csv(tfsfile, delim_whitespace=True, nrows=45, index_col=None)
    headerdata.columns = ["AT", "NAME", "TYPE", "VALUE"]
    return headerdata[["NAME", "VALUE"]]


def get_twissdata(tfsfile):
    """
    Get the actual table data of the twiss data
    :param tfsfile: file where the twiss data is stored
    :return: dataframe containing the twiss table data
    """
    data = pd.read_csv(tfsfile, delim_whitespace=True, skiprows=48, index_col=None, header=None)
    data.columns = get_twisscolumns(tfsfile)
    return data


def get_survey_columns(tfssurveyfile):
    """
    Reads the headers of the columns of the survey file
    :param tfssurveyfile:  file where survey output is stored
    :return: list of strings
    """
    cols = pd.read_csv(
        tfssurveyfile, delim_whitespace=True, skiprows=range(6), nrows=2, index_col=None
    )
    return cols.columns[1:].values


def get_survey_data(tfssurveyfile):
    """
    Get the actual table data of the twiss data
    :param tfssurveyfile: file where the twiss data is stored
    :return: dataframe containing the twiss table data
    """
    data = pd.read_csv(
        tfssurveyfile, delim_whitespace=True, skiprows=8, index_col=None, header=None
    )
    data.columns = get_survey_columns(tfssurveyfile)
    return data
