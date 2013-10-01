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
    install_requires=['anyjson==0.3.3', 'requests==1.1.0', 'beautifulsoup4==4.3.1'],
    packages=['scalpyr', ],
    license="MIT",
    long_description="",
    download_url='https://github.com/spothero/scalpyr/tarball/0.0.1',
    keywords=['api', 'SeatGeek'])


