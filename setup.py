from setuptools import setup

setup(
    name='youjunk',
    version='1.0',
    packages=['yourapplication'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)
