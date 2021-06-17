import setuptools

# esto se actualiza solo con https://python-semantic-release.readthedocs.io/en/latest/index.html
__version__ = "0.7.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hexagon",
    version=__version__,
    author="Joaco Campero",
    author_email="joaquin@redbee.io",
    description="Una CLI para generar CLIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/redbeestudios/hexagon",
    project_urls={
        "Bug Tracker": "https://github.com/redbeestudios/hexagon/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "inquirerpy",
        "rich",
        "clipboard",
        "requests",
        "ruamel.yaml",
    ],
    python_requires=">=3.6",
    entry_points='''
        [console_scripts]
        hexagon=hexagon.__main__:main
    ''',
    platform="debian"
)
