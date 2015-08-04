from setuptools import setup

setup(
    name='relevantxkcd',
    version='0.1',
    packages=['relevantxkcd'],
    url='https://www.github.com/brettvitaz/relevantxkcd',
    license='nunya',
    author='brettvitaz',
    author_email='brett@vitaz.net',
    description='Relevant XKCD api',
    keywords='relevant xkcd',
    classifiers=['Development Status :: 3 - Alpha'],
    install_requires=['bottle>=0.12.5', 'waitress>=0.8.8', 'requests>=2.7.0', 'sqlalchemy', 'alembic', 'apscheduler'],
)
