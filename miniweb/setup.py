from setuptools import setup


setup(
    name="miniweb",
    description="Web application framework for Micropython.",
    version="1.0.1",
    author="Martin Masata",
    author_email="martin.masata98@gmail.com",
    packages=['core', 'entity', 'exception', 'message', 'tools'],
    keywords="micropython webapp miniweb rest route"
)
