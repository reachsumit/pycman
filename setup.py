import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycman",
    version="0.7",
    author="Sumit Kumar (Arora)",
    author_email="sam.sumitkumar@gmail.com",
    description="Pacman game simulator in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/reachsumit/pycman",
    packages=setuptools.find_packages(),
    install_requires=[
          'click',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
