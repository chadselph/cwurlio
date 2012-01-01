from setuptools import setup, find_packages

setup(
    name = "cwurlio",
    version = "0.1",
    packages = find_packages(),
    scripts = ['scripts/cwurlio.py'],
    install_requires = ['twilio>=3.0.0'],
    author = "Chad Selph",
    description = "Replacement for curl when testing twilio apps"
)
