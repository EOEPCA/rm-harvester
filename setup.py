from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
#     long_description = fh.read()


long_description = ""

setup(
    name="harvester_eoepca",
    version="1.0.0-rc.1",
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EOEPCA/rm-harvester/tree/master",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
