from setuptools import setup, find_packages
import os
def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()
setup (
    name="MethPy",
    version="2025.1",
    packages=find_packages(),
    long_description= read ("README.md"),
    long_description_content_type="text/markdown"
)
