import os

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# automatically captured required modules for install_requires in requirements.txt
with open('requirements.txt', encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if
                    ('git+' not in x) and (not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

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
    install_requires=install_requires,
    dependency_links=dependency_links,
    python_requires=">=3.6",
    entry_points='''
        [console_scripts]
        hexagon=src.hexagon.__main__:main
    ''',
    platform="debian"
)
