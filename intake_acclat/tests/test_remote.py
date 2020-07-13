import os
import subprocess
import time

import intake
import pytest
import requests

PORT = 8425
here = os.path.abspath(os.path.dirname(__file__))
cat_file = os.path.join(here, "data", "catalog.yaml")


@pytest.fixture(scope="module")
def intake_server():
    command = ["intake-server", "-p", str(PORT), cat_file]
    try:
        P = subprocess.Popen(command)
        timeout = 10
        while True:
            try:
                requests.get("http://localhost:{}".format(PORT))
                break
            except:
                time.sleep(0.1)
                timeout -= 0.1
                assert timeout > 0
        yield "intake://localhost:{}".format(PORT)
    finally:
        P.terminate()
        P.communicate()


def test_remote(intake_server):
    import pandas as pd

    # cat_local = intake.open_catalog(cat_file)
    cat = intake.open_catalog(intake_server)
    assert "fodo" in cat
    source = cat.fodo()
    assert source._schema is not None
    assert isinstance(source.read(), dict)
    assert isinstance(source.to_madx(), str)
    assert isinstance(source.to_lte(), str)
    assert isinstance(source.to_twiss(), pd.DataFrame)
