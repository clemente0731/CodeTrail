from setuptools import setup, find_packages


def read_requirements(file_path):
    # read requirements from file
    # args: file_path (str): path to requirements file
    # returns: list of requirement names
    with open(file_path) as f:
        requirements = f.read().splitlines()
        print("codet install_requires:", requirements)
        return requirements


setup(
    name="codet",
    version="1.0.0",
    description="A repository code trail tool",
    long_description="A repository code trail tool",
    url="https://www.codetrail.com/codetrail",
    author="clemente0620",
    author_email="clemente0620@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "codet=codet.cli.codet:main",
        ]
    },
    packages=find_packages(exclude=["codet/tests"]),
    include_package_data=True,
    install_requires=read_requirements("./requirements.txt"),
    zip_safe=False,
)
