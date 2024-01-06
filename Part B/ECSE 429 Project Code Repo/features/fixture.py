import os
import subprocess
import sys

from behave import fixture


@fixture(name="fixture.app")
def app(context):
    if os.getenv("ABNORMAL", "false") == "true":
        yield
    else:
        process = subprocess.Popen(
            ["starter.bat"],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        status_code = subprocess.call(["curl", "http://localhost:4567"], shell=True)
        while status_code:
            status_code = subprocess.call(
                ["curl", "http://localhost:4567"],
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )
        yield process

        subprocess.call(
            ["curl", "http://localhost:4567/shutdown"],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        process.kill()
