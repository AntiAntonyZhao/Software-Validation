import os
import subprocess
import pytest


@pytest.fixture(scope="function")
def client():
    if os.getenv("ABNORMAL", False):
        yield
    else:
        process = subprocess.Popen(["starter.bat"], shell=True)
        status_code = subprocess.call(["curl", "http://localhost:4567"], shell=True)
        while status_code:
            status_code = subprocess.call(["curl", "http://localhost:4567"], shell=True)
        yield
        subprocess.call(["curl", "http://localhost:4567/shutdown"], shell=True)
        process.kill()
