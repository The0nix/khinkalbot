from setuptools import setup, find_packages

setup(
    name="khinkalbot",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "aiogram",
        "peewee",
        "flask",
        "flask-admin",
        "flask-basicauth",
        "wtf-peewee",
    ],
    entry_points={
        "console_scripts": [
            "khinkalbot = khinkalbot.__main__:cli",
        ],
    },
)
