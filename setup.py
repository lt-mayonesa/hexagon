import setuptools
import json
import glob

# esto se actualiza solo con https://python-semantic-release.readthedocs.io/en/latest/index.html
__version__ = "0.22.1"


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

translations = glob.glob("./locales/*/LC_MESSAGES/*.mo")

setuptools.setup(
    name="hexagon",
    version=__version__,
    author="Joaco Campero",
    author_email="joaquin@redbee.io",
    description="Una CLI para generar CLIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/redbeestudios/hexagon",
    project_urls={"Bug Tracker": "https://github.com/redbeestudios/hexagon/issues"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["tests", "tests.*", "e2e", "e2e.*"]),
    package_data={"": ["*.md"]},
    install_requires=requires,
    python_requires=">=3.7",
    entry_points="""
        [console_scripts]
        hexagon=hexagon.__main__:main
    """,
    platform="debian",
    data_files=[("*", ["Pipfile.lock"]), ("locales", translations)],
)
