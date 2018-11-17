import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-grpc",
    version=os.environ.get("SIMPLE_VERSION", "0.0.1"),
    author="Shuttl, LLC",
    author_email="hello@shuttl.io",
    description="A simple way to define gRPC patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shuttl-io/simple-grpc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
