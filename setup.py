import glob
import json
from os.path import dirname

import setuptools

# this updates automatically https://python-semantic-release.readthedocs.io/en/latest/index.html
__version__ = "0.58.1"


def __markers(config: dict):
    return f"; {config['markers']}" if "markers" in config else ""


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("Pipfile.lock", "r", encoding="utf-8") as lock:
    json_lock = json.load(lock)
    requires = [
        f"{name}{config['version']}{__markers(config)}"
        for name, config in json_lock["default"].items()
        if "version" in config
    ]

translations = [(dirname(x), [x]) for x in glob.glob("locales/*/LC_MESSAGES/*.mo")]

setuptools.setup(
    name="hexagon",
    version=__version__,
    author="Joaco Campero",
    author_email="juacocampero@gmail.com",
    description="Build your Team's CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lt-mayonesa/hexagon",
    project_urls={"Bug Tracker": "https://github.com/lt-mayonesa/hexagon/issues"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(
        exclude=["tests", "tests.*", "tests_e2e", "tests_e2e.*"]
    ),
    include_package_data=True,
    install_requires=requires,
    python_requires=">=3.9",
    entry_points="""
        [console_scripts]
        hexagon=hexagon.__main__:main
    """,
    data_files=translations,
)
