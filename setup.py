from setuptools import setup, find_packages

# Files are already in the repo, no copying needed
setup(
    packages=find_packages(),
    package_data={
        'pyeudaq': ['*.so', '*.pyd', '*.dylib', 'lib/*.so*'],
    },
    include_package_data=True,
)
