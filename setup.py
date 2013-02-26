__version__ = (0, 0, 1)

try:
    from setuptools import setup
except ImportError:
    from disutils.core import setup

setup(
    name="scalpyr",
    version='.'.join(str(x) for x in __version__),
    description="Easily access the Seatgeek API in pure Python",
    url="https://github.com/yolesaber/scalpyr",
    author="Michael Anzuoni",
    author_email="me.anzuoni@gmail.com",
    install_requires=['json==2.0.9', 'requests==1.1.0'],
    packages=['link', ],
    license="MIT",
    long_description="")


