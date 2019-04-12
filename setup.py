import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='flaskr',
    version='1.0.0',
    author="Ketan Sharma ( CSEVIRUS )",
    author_email="ketansharma144@gmail.com",
    description="A variation of online judge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/csevirus/bc",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'flask',
    ],
)
