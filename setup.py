import os

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hexagon",
    version=os.getenv("RELEASE_VERSION", "0.0.1"),
    author="Joaco Campero",
    author_email="joaquin@redbee.ioo",
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
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "inquirerpy",
        "rich",
        "pyyaml",
        "clipboard",
        "requests",
    ],
    python_requires=">=3.6",
    entry_points='''
        [console_scripts]
        hexagon=hexagon.__main__:main
    ''',
    platform="debian"
)
