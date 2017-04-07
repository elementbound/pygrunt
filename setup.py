from setuptools import setup, find_packages

exec(open('pygrunt/version.py').read())

setup(
    name="pygrunt",
    version=version_str,
    packages=find_packages(),

    install_requires=["colorama >=0.3.7"],

    author="Tamás Gálffy",
    author_email="tamasgalffy@gmail.com",
    description="A C/C++ build system written in Python",
    license="GNU GPL v3",
    url="https://github.com/elementbound/pygrunt",

    entry_points={
        "console_scripts": [
            "pygrunt = pygrunt.run:run"
        ]
    },

    classifiers=[
        'Programming Language :: Python :: 3'
        # TODO: more classifiers
    ]
)
