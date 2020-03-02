""" Setup script for package. """
from setuptools import setup, find_packages

setup(
    name="Image Patch Reconstructor",
    author="Marija Vella, Matthew Aquilina",
    description="Package which reconstructs images from patches with a variable stride length.",
    url="https://github.com/marijavella/image-reconstructor-patches",
    packages=find_packages(),
)

